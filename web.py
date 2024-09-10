from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))

    def get_response(self):
        # Extraer el path y la query string
        path = self.url().path.strip('/')
        query_params = self.query_data()

        # DEBUG: Imprimir los parámetros para revisar si se están capturando correctamente
        print(f"Path: {path}")
        print(f"Query Params: {query_params}")

        # Obtener el valor del parámetro 'autor', si existe
        autor = query_params.get('autor', 'Desconocido')

        # Crear la respuesta HTML dinámica
        return f"""
        <h1>Proyecto: {path} Autor: {autor}</h1>
        <p> URL Parse Result : {self.url()} </p>
        <p> Path Original: {self.path} </p>
        <p> Headers: {self.headers} </p>
        <p> Query: {query_params} </p>
        """
       #return f"""
    #<h1> Hola Web </h1>
    #<p> URL Parse Result : {self.url()}         </p> 
    #<p> Path Original: {self.path}         </p>
    #<p> Headers: {self.headers}      </p>
   # <p> Query: {self.query_data()}   </p>
#"""


if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
