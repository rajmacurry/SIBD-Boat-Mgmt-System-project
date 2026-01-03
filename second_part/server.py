from http.server import HTTPServer, CGIHTTPRequestHandler
import sys

# Define a custom handler that treats the root directory as CGI-enabled
class CustomCGIHandler(CGIHTTPRequestHandler):
    # This list defines which directories contain CGI scripts. 
    # By adding '/', we tell the server that scripts in the root directory can be executed.
    cgi_directories = ['/']

    def is_python(self, path):
        """Test whether argument path is a Python script."""
        return path.lower().endswith('.cgi') or path.lower().endswith('.py')

def run(server_class=HTTPServer, handler_class=CustomCGIHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting customizable CGI Server on port {port}...")
    print(f"Scripts in the current directory will be executed.")
    print("Press Ctrl+C to stop.")
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nServer stopped.")
