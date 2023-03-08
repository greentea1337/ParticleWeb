import logging
import ssl
from http.server import HTTPServer
from socketserver import ThreadingMixIn
from request_handler import RequestHandler
from threaded_http_server import ThreadedHTTPServer

class Server:
    def __init__(self, host='192.168.0.161', port=8080, https=False):
        self.host = host
        self.port = port
        self.https = https
        self.server_class = HTTPServer if not https else None
        self.ssl_context = None if not https else ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        if https:
            self.ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    def start(self):
        self.server_class = ThreadedHTTPServer if not self.https else self.server_class
        self.server_address = (self.host, self.port)
        self.httpd = self.server_class(self.server_address, RequestHandler)
        if self.https:
            self.httpd.socket = self.ssl_context.wrap_socket(self.httpd.socket, server_side=True)
        protocol = "HTTPS" if self.https else "HTTP"
        logging.info(f'Starting {protocol} server on port {self.port}...')
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        self.httpd.server_close()
        logging.info('Server stopped.')