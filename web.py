from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qsl

#Sitio Web Dinámico
# Diccionario con el contenido HTML para otras rutas
contenido = {
    '/proyecto/1': """
    <html>
    <head>
        <title>Web Estática - App de recomendación de libros</title>
    </head>
    <body>
        <h1>Web Estática - App de recomendación de libros</h1>
    </body>
    </html>""",
    '/proyecto/2': """
    <html>
    <head>
        <title>Web App - MeFalta</title>
    </head>
    <body>
        <h1>Web App - MeFalta</h1>
    </body>
    </html>""",
    '/proyecto/3': """
    <html>
    <head>
        <title>Web App - Foto22</title>
    </head>
    <body>
        <h1>Web App - Foto22</h1>
    </body>
    </html>"""
}

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def do_GET(self):
        path = self.url().path

        if path == '/':
            # Servir home.html para la ruta principal
            self.serve_home()
        elif path in contenido:
            # Servir contenido HTML desde el diccionario para otras rutas
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            response_content = contenido[path]
            self.wfile.write(response_content.encode("utf-8"))
        elif path.startswith('/proyecto/'):
            # Servir contenido dinámico para rutas de proyecto con parámetros
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            response_content = self.get_dynamic_content()
            self.wfile.write(response_content.encode("utf-8"))
        else:
            # Servir 404 para rutas no encontradas
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def serve_home(self):
        try:
            with open('home.html', 'r') as file:
                content = file.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def get_dynamic_content(self):
        # Extraer la query string (autores y parámetros)
        query_params = dict(parse_qsl(self.url().query))
        autor = query_params.get('autor', 'Desconocido')

        # Crear la respuesta HTML dinámica para las páginas de proyecto
        return f"""
        <html>
        <head><title>Proyecto Dinámico</title></head>
        <body>
            <h1>Hola, este proyecto es de {autor}.</h1>
            <ul>
                <li><a href="/proyecto/1">Web Estática - App de recomendación de libros</a></li>
                <li><a href="/proyecto/2">Web App - MeFalta</a></li>
                <li><a href="/proyecto/3">Web App - Foto22</a></li>
            </ul>
            <p> URL Parse Result: {self.url()} </p> 
            <p> Path Original: {self.path} </p>
            <p> Headers: {self.headers} </p>
            <p> Query: {self.url().query} </p>
            <p> Autor: {autor} </p>
        </body>
        </html>
        """
if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
    
