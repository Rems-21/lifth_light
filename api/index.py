"""
Vercel serverless function handler for Django
Compatible with Vercel Python runtime
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

def handler(req):
    """
    Vercel serverless function handler for Django WSGI
    Compatible with Vercel Python Request/Response format
    """
    # Vercel Python passes a Request object with:
    # - req.method
    # - req.path
    # - req.headers (dict-like)
    # - req.body (bytes or None)
    # - req.query (dict)
    
    # Extract request data
    method = req.method if hasattr(req, 'method') else 'GET'
    path = req.path if hasattr(req, 'path') else '/'
    query = req.query if hasattr(req, 'query') else {}
    headers = dict(req.headers) if hasattr(req, 'headers') else {}
    body = req.body if hasattr(req, 'body') and req.body else b''
    
    # Build query string
    query_string = '&'.join([f'{k}={v}' for k, v in query.items()]) if query else ''
    
    # Build WSGI environ
    environ = {
        'REQUEST_METHOD': method,
        'SCRIPT_NAME': '',
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('content-type', headers.get('Content-Type', '')),
        'CONTENT_LENGTH': str(len(body)) if body else '',
        'SERVER_NAME': headers.get('host', headers.get('Host', 'localhost')).split(':')[0],
        'SERVER_PORT': headers.get('host', headers.get('Host', 'localhost')).split(':')[1] if ':' in headers.get('host', headers.get('Host', '')) else '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https' if headers.get('x-forwarded-proto', headers.get('X-Forwarded-Proto', '')) == 'https' else 'http',
        'wsgi.input': BytesIO(body) if body else BytesIO(),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add HTTP headers to environ
    for key, value in headers.items():
        key_upper = key.upper().replace('-', '_')
        if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key_upper}'] = value
    
    # Response storage
    response_status = 200
    response_headers_list = []
    
    def start_response(status, headers_list):
        nonlocal response_status, response_headers_list
        response_status = int(status.split()[0])
        response_headers_list = headers_list
    
    # Call WSGI application
    try:
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
        
        # Convert headers to dict (Vercel format)
        response_headers_dict = {}
        for header, value in response_headers_list:
            # Vercel expects lowercase header names
            response_headers_dict[header.lower()] = value
        
        # Return Vercel response format
        return {
            'statusCode': response_status,
            'headers': response_headers_dict,
            'body': body_bytes.decode('utf-8', errors='ignore')
        }
    except Exception as e:
        # Error handling
        import traceback
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        return {
            'statusCode': 500,
            'headers': {'content-type': 'text/plain'},
            'body': error_msg
        }
