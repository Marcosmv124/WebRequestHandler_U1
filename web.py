from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

   def do_GET(self):
      # self.send_response(200)
       #self.send_header("Content-Type", "text/html")
       #self.end_headers()
       #self.wfile.write(self.get_response().encode("utf-8"))
          # Determinar si se solicita la página de inicio o una ruta no definida
        if self.url().path == '/':
            self.serve_home()
        else:
            self.serve_404()

      def serve_home(self):
        # Leer el contenido del archivo home.html
        try:
            with open('home.html', 'r') as file:
                contenido = file.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(contenido.encode('utf-8'))
        except FileNotFoundError:
            self.serve_404()
        
      def serve_404(self):
        # Leer el contenido del archivo 404.html
        try:
            with open('404.html', 'r') as file:
                contenido = file.read()
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(contenido.encode('utf-8'))
        except FileNotFoundError:
            # Fallback si no se encuentra 404.html
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 No Encontrado")

    def get_response(self):
    # Extraer el path y la query string
      path = self.url().path.strip('/')
        query_params = self.query_data()
        #DEBUG: Imprimir los parámetros para revisar si se están capturando correctamente
        print(f"Path: {path}")
        print(f"Query Params: {query_params}")

        # Obtener el valor del parámetro 'autor', si existe
       autor = query_params.get('autor', 'Desconocido')

        #Crear la respuesta HTML dinámica
       return f"""
    <h1> Hola Web </h1>
    <p> URL Parse Result : {self.url()}         </p> 
    <p> Path Original: {self.path}         </p>
    <p> Headers: {self.headers}      </p>
    <p> Query: {self.query_data()}   </p>
"""

if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
