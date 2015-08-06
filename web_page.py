# -*-coding: utf8-*

import socket
from wsgiref.simple_server import make_server


def hello_world_app(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/plain; charset=utf-8')] # HTTP Headers
    start_response(status, headers)

    # The returned object is going to be printed
    return [b"Hello World"]


def main():
    PORT = 8000
    HEBERGEUR = socket.gethostbyname(socket.gethostname())
    httpd = make_server(HEBERGEUR, PORT, hello_world_app)
    print("Pour quitter, appuyer sur CTRL+C\n")

    print("IP locale    ::  " + HEBERGEUR)
    print("Port utilisé ::  " + str(PORT))
    httpd.serve_forever()
