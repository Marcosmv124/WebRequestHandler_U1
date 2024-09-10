from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qsl

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def do_GET(self):
        path = self.url().path
        if path == '/':
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            response_content = self.get_home_content()
            self.wfile.write(response_content.encode("utf-8"))
        else:
            self.send_error_page()

    def get_home_content(self):
        try:
            with open('home.html', 'r') as file:
                return file.read()
        except FileNotFoundError:
            # Si no se puede encontrar home.html, retorna una página de error
            return "404 Not Found"

    def send_error_page(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        
        try:
            with open('404.html', 'r') as file:
                content = file.read()
            self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            # En caso de que el archivo 404.html también falte
            self.wfile.write(b"<h1>404 Not Found</h1>")

if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()s
