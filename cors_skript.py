import http.server
import socketserver
import os
import sys

def start_server(port, directory):
    """
    Start a CORS-enabled HTTP server
    
    Parameters:
    -----------
    port : int
        Port to use for the server
    directory : str
        Directory to serve files from
    """
    class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
        
        def end_headers(self):
            # Add CORS headers
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            super().end_headers()
        
        def do_OPTIONS(self):
            # Handle OPTIONS request (pre-flight)
            self.send_response(200)
            self.end_headers()

    print(f"Starting CORS-enabled server on port {port}...")
    print(f"Serving files from: {directory}")
    
    Handler = CORSRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        httpd.server_close()

# Allow the script to be run directly
if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) >= 3:
        port = int(sys.argv[1])
        directory = sys.argv[2]
        start_server(port, directory)
    else:
        print("Usage: python cors_http_server.py <port> <directory>")
        sys.exit(1)