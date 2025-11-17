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

# Log startup
print(f"Starting handler, BASE_DIR: {BASE_DIR}", file=sys.stderr)
print(f"Python version: {sys.version}", file=sys.stderr)
print(f"Python path: {sys.path[:3]}", file=sys.stderr)

# Set Django settings module
settings_file = os.path.join(BASE_DIR, 'liftandlight', 'settings_vercel.py')
if os.path.exists(settings_file):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liftandlight.settings_vercel')
    print("Using settings_vercel", file=sys.stderr)
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liftandlight.settings')
    print("Using default settings", file=sys.stderr)

# Try to import and setup Django
django_ready = False
application = None
error_message = None
error_traceback = None

try:
    print("Importing django...", file=sys.stderr)
    import django
    print(f"Django version: {django.get_version()}", file=sys.stderr)
    print("Calling django.setup()...", file=sys.stderr)
    django.setup()
    print("Django setup complete", file=sys.stderr)
    
    # Import WSGI application
    print("Importing WSGI application...", file=sys.stderr)
    from liftandlight.wsgi import application
    print("WSGI application imported successfully", file=sys.stderr)
    django_ready = True
except Exception as e:
    error_message = str(e)
    import traceback
    error_traceback = traceback.format_exc()
    print(f"Django setup error: {error_message}", file=sys.stderr)
    print(error_traceback, file=sys.stderr)
    django_ready = False
    application = None

def handler(request):
    """
    Vercel serverless function handler for Django WSGI
    """
    # If Django failed to initialize, return detailed error
    if not django_ready:
        error_html = f'''<html><head><title>Django Initialization Error</title></head><body>
            <h1>Django Initialization Error</h1>
            <h2>Error Message:</h2>
            <pre>{error_message}</pre>
            <h2>Traceback:</h2>
            <pre>{error_traceback}</pre>
            <h2>Environment:</h2>
            <ul>
                <li>BASE_DIR: {BASE_DIR}</li>
                <li>DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}</li>
                <li>Python: {sys.version}</li>
            </ul>
        </body></html>'''
        return {
            'statusCode': 500,
            'headers': {'content-type': 'text/html; charset=utf-8'},
            'body': error_html
        }
    
    try:
        # Log request info
        print(f"Request received: {type(request)}", file=sys.stderr)
        
        # Extract request data - Vercel Python Request object
        method = getattr(request, 'method', 'GET')
        path = getattr(request, 'path', '/')
        
        # Try to get URL if path is not available
        if path == '/' and hasattr(request, 'url'):
            from urllib.parse import urlparse
            parsed = urlparse(request.url)
            path = parsed.path or '/'
        
        print(f"Method: {method}, Path: {path}", file=sys.stderr)
        
        # Get headers
        headers = {}
        if hasattr(request, 'headers'):
            try:
                if isinstance(request.headers, dict):
                    headers = request.headers
                elif hasattr(request.headers, 'items'):
                    headers = dict(request.headers.items())
                else:
                    headers = dict(request.headers)
            except Exception as e:
                print(f"Error reading headers: {e}", file=sys.stderr)
        
        # Get body
        body = b''
        if hasattr(request, 'body'):
            if request.body:
                if isinstance(request.body, bytes):
                    body = request.body
                elif isinstance(request.body, str):
                    body = request.body.encode('utf-8')
        
        # Get query string
        query_string = ''
        if hasattr(request, 'query') and request.query:
            query_parts = []
            if isinstance(request.query, dict):
                for k, v in request.query.items():
                    if isinstance(v, list):
                        for val in v:
                            query_parts.append(f'{k}={val}')
                    else:
                        query_parts.append(f'{k}={v}')
            query_string = '&'.join(query_parts)
        elif hasattr(request, 'url') and '?' in request.url:
            query_string = request.url.split('?', 1)[1]
        
        # Build WSGI environ
        host = headers.get('host', headers.get('Host', 'localhost'))
        if isinstance(host, list):
            host = host[0] if host else 'localhost'
        host_str = str(host)
        server_name = host_str.split(':')[0] if ':' in host_str else host_str
        server_port = host_str.split(':')[1] if ':' in host_str else '80'
        
        environ = {
            'REQUEST_METHOD': str(method),
            'SCRIPT_NAME': '',
            'PATH_INFO': str(path),
            'QUERY_STRING': str(query_string),
            'CONTENT_TYPE': str(headers.get('content-type', headers.get('Content-Type', ''))),
            'CONTENT_LENGTH': str(len(body)) if body else '',
            'SERVER_NAME': server_name,
            'SERVER_PORT': server_port,
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
            key_upper = str(key).upper().replace('-', '_')
            if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                environ[f'HTTP_{key_upper}'] = str(value)
        
        # Response storage
        response_status = 200
        response_headers_list = []
        
        def start_response(status, headers_list):
            nonlocal response_status, response_headers_list
            response_status = int(str(status).split()[0])
            response_headers_list = headers_list
        
        # Call WSGI application
        print("Calling WSGI application...", file=sys.stderr)
        result = application(environ, start_response)
        print(f"WSGI application returned, status: {response_status}", file=sys.stderr)
        
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
        
        # Convert headers to dict (Vercel format - lowercase keys)
        response_headers_dict = {}
        for header, value in response_headers_list:
            response_headers_dict[str(header).lower()] = str(value)
        
        print(f"Returning response, status: {response_status}, body length: {len(body_bytes)}", file=sys.stderr)
        
        # Return Vercel response format
        return {
            'statusCode': response_status,
            'headers': response_headers_dict,
            'body': body_bytes.decode('utf-8', errors='ignore')
        }
        
    except Exception as e:
        # Error handling with detailed traceback
        import traceback
        error_msg = f"Handler Error: {type(e).__name__}: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(error_msg, file=sys.stderr)
        return {
            'statusCode': 500,
            'headers': {'content-type': 'text/html; charset=utf-8'},
            'body': f'''<html><head><title>Handler Error</title></head><body>
                <h1>Handler Error</h1>
                <pre>{error_msg}</pre>
            </body></html>'''
        }
