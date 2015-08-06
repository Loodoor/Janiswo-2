from urllib import request
import socketserver
import http.server
import socket


PORT = 8000
HEBERGEUR = socket.gethostbyname(socket.gethostname())


class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.copyfile(request.urlopen(self.path), self.wfile)


def main():
    print("IP locale    ::  " + HEBERGEUR)
    print("Port utilisé ::  " + str(PORT))
    httpd = socketserver.ForkingTCPServer((HEBERGEUR, PORT), Proxy)
    httpd.serve_forever()