"""
Emergency WSGI application for diagnosing Railway deployment issues.
This script provides a minimal WSGI application that bypasses the Django framework
to help diagnose issues with the deployment.

To use this in Railway:
1. Add this file to your project
2. Update the Procfile or Railway configuration to use this file:
   `web: gunicorn backend.emergency:application --log-file -`
"""

import os
import sys
import json
import traceback
import datetime
from pathlib import Path

def application(environ, start_response):
    """
    Minimal WSGI application to diagnose deployment issues
    """
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    
    try:
        # Get information about the environment
        path_info = environ.get('PATH_INFO', '/')
        
        # Simple router
        if path_info == '/debug-env':
            # Return environment variables as JSON
            response_body = json.dumps({
                "environ": {k: str(v) for k, v in sorted(environ.items())},
                "os_environ": {k: str(v) for k, v in sorted(os.environ.items())},
                "sys_path": sys.path,
                "python_version": sys.version,
                "timestamp": datetime.datetime.now().isoformat(),
                "cwd": os.getcwd(),
                "file_location": str(Path(__file__).resolve()),
            }, indent=2)
            headers = [('Content-type', 'application/json')]
        elif path_info == '/test-media':
            # Check if media directory exists
            media_root = os.environ.get('MEDIA_ROOT', 'media')
            media_exists = os.path.exists(media_root)
            media_info = {
                "media_root": media_root,
                "media_exists": media_exists,
                "media_contents": os.listdir(media_root) if media_exists else []
            }
            response_body = json.dumps(media_info, indent=2)
            headers = [('Content-type', 'application/json')]
        else:
            # Basic HTML response
            response_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Emergency Diagnostics</title>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 20px; }}
                    h1 {{ color: #e74c3c; }}
                    pre {{ background: #f8f9fa; padding: 10px; overflow: auto; }}
                    .button {{ display: inline-block; padding: 8px 16px; margin: 5px; 
                              background: #3498db; color: white; text-decoration: none; border-radius: 4px; }}
                </style>
            </head>
            <body>
                <h1>Railway Emergency Diagnostic Mode</h1>
                <p>This is an emergency diagnostic mode for troubleshooting Railway deployment issues.</p>
                
                <h2>System Information</h2>
                <pre>
Python Version: {sys.version}
Current Time: {datetime.datetime.now()}
Working Directory: {os.getcwd()}
This File: {Path(__file__).resolve()}
                </pre>
                
                <h2>Diagnostic Tools</h2>
                <a href="/debug-env" class="button">View Environment Details</a>
                <a href="/test-media" class="button">Test Media Directory</a>
                
                <h2>Request Information</h2>
                <pre>
Path: {environ.get('PATH_INFO')}
Method: {environ.get('REQUEST_METHOD')}
Query String: {environ.get('QUERY_STRING')}
Server: {environ.get('SERVER_NAME')}:{environ.get('SERVER_PORT')}
Remote: {environ.get('REMOTE_ADDR')}
                </pre>
                
                <h2>Next Steps</h2>
                <p>After identifying the issue:</p>
                <ol>
                    <li>Fix the configurations in Railway</li>
                    <li>Update your code repository</li>
                    <li>Revert to your regular WSGI application</li>
                </ol>
            </body>
            </html>
            """
            
        response = response_body.encode('utf-8')
        
    except Exception as e:
        # If anything goes wrong, display the error
        status = '500 Internal Server Error'
        error_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error</title>
            <style>
                body {{ font-family: sans-serif; margin: 20px; }}
                h1 {{ color: #e74c3c; }}
                pre {{ background: #f8f9fa; padding: 10px; overflow: auto; }}
            </style>
        </head>
        <body>
            <h1>Emergency Diagnostic Error</h1>
            <p>An error occurred in the emergency diagnostic application:</p>
            <pre>{str(e)}</pre>
            <h2>Traceback</h2>
            <pre>{traceback.format_exc()}</pre>
        </body>
        </html>
        """
        response = error_message.encode('utf-8')
        headers = [('Content-type', 'text/html; charset=utf-8')]
    
    start_response(status, headers)
    return [response]

if __name__ == '__main__':
    # This block allows the file to be run directly for testing
    from wsgiref.simple_server import make_server
    
    port = 8000
    print(f"Starting emergency diagnostic server on port {port}...")
    httpd = make_server('', port, application)
    print(f"Go to http://localhost:{port}/ for diagnostic information")
    httpd.serve_forever() 