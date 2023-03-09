import os
from http.server import SimpleHTTPRequestHandler
from threaded_http_server import ThreadedHTTPServer
import logging

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='pages', **kwargs)

    def do_GET(self):
        file_path = self.translate_path(self.path)
        if os.path.isfile(file_path):
            self.send_response(200)
            content_type = self.get_content_type(file_path)
            self.send_header('Content-type', content_type)
            self.end_headers()
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'File Not Found')

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(content_length)
        # Handle the data here, e.g. parse it, write it to a file, etc.
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'POST request received')

    def get_content_type(self, file_path):
        if file_path.endswith('.html'):
            return 'text/html'
        elif file_path.endswith('.css'):
            return 'text/css'
        elif file_path.endswith('.js'):
            return 'text/javascript'
        else:
            return 'text/plain'
