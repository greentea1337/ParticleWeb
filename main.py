import argparse
from server import Server
from threaded_http_server import ThreadedHTTPServer
print("The server has been successfully launched!")
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--https", action="store_true", help="Enable HTTPS support")
    args = parser.parse_args()

    server = Server(https=args.https)
    server.start()

if __name__ == '__main__':
    main()