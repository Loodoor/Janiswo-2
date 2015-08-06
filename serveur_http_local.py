# -*-coding: utf8-*

import http.server
import socketserver
import socket
from urllib.request import urlopen


def main():
    PORT = 8000
    HEBERGEUR = socket.gethostbyname(socket.gethostname())
    IP = urlopen('http://ip.42.pl/raw').read()

    Handler = http.server.SimpleHTTPRequestHandler

    httpd = socketserver.TCPServer((HEBERGEUR, PORT), Handler)
    
    print("Pour quitter, appuyer sur CTRL+C\n")

    print("IP locale    ::  " + HEBERGEUR)
    print("Port utilisé ::  " + str(PORT))
    print("IP publique  ::  " + IP.decode() + "\n")

    httpd.serve_forever()