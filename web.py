from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qsl

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def do_GET(self):
        path = self.url().path
        if path == '/':
            # Servir home.html para la ruta principal
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            response_content = self.get_home_content()
            self.wfile.write(response_content.encode("utf-8"))
        else:
            # Para otras rutas, generar contenido dinámico basado en los parámetros
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            response_content = self.get_dynamic_content()
            self.wfile.write(response_content.encode("utf-8"))
#home page
    def get_home_content(self):
        try:
            with open('home.html', 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "404 Not Found"

    def get_dynamic_content(self):
        # Extraer la query string
        query_params = dict(parse_qsl(self.url().query))

        # Obtener el valor del parámetro 'autor', si existe
        autor = query_params.get('autor', 'Desconocido')

        # Crear la respuesta HTML dinámica
        return f"""
<h1> Hola Web </h1>
<p> URL Parse Result : {self.url()} </p> 
<p> Path Original: {self.path} </p>
<p> Headers: {self.headers} </p>
<p> Query: {self.url().query} </p>
<p> Autor: {autor} </p>
"""

if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
    
