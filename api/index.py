"""
Vercel serverless function handler for Django
"""
import os
import sys
from pathlib import Path
from io import BytesIO

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liftandlight.settings')

# Import Django
import django
django.setup()

# Import WSGI application
from liftandlight.wsgi import application

def handler(request):
    """
    Vercel serverless function handler for Django WSGI
    """
    # Get request data
    method = request.method
    path = request.path
    query_string = request.query_string if hasattr(request, 'query_string') else ''
    headers = dict(request.headers) if hasattr(request, 'headers') else {}
    body = request.body if hasattr(request, 'body') else b''
    
    # Build WSGI environ
    environ = {
        'REQUEST_METHOD': method,
        'SCRIPT_NAME': '',
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('Content-Type', ''),
        'CONTENT_LENGTH': str(len(body)) if body else '',
        'SERVER_NAME': headers.get('Host', 'localhost').split(':')[0],
        'SERVER_PORT': headers.get('Host', 'localhost').split(':')[1] if ':' in headers.get('Host', '') else '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https' if headers.get('X-Forwarded-Proto') == 'https' else 'http',
        'wsgi.input': BytesIO(body) if body else BytesIO(),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add HTTP headers
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key}'] = value
    
    # Response storage
    response_status = 200
    response_headers = []
    
    def start_response(status, headers_list):
        nonlocal response_status, response_headers
        response_status = int(status.split()[0])
        response_headers = headers_list
    
    # Call WSGI application
    result = application(environ, start_response)
    
    # Collect response body
    body_parts = []
    for part in result:
        if isinstance(part, bytes):
            body_parts.append(part)
        else:
            body_parts.append(str(part).encode('utf-8'))
    
    if hasattr(result, 'close'):
        result.close()
    
    body_bytes = b''.join(body_parts)
    
    # Convert headers to dict
    response_headers_dict = {}
    for header, value in response_headers:
        response_headers_dict[header] = value
    
    # Return Vercel response format
    return {
        'statusCode': response_status,
        'headers': response_headers_dict,
        'body': body_bytes.decode('utf-8', errors='ignore')
    }
