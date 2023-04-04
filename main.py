#!/usr/bin/python
import os
import base64
import random
import string
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write(b'no auth header received')
            pass
        elif self.headers.get('Authorization') == 'Basic ' + str(self.server.auth):
            try:
                # print(os.path.basename(__file__))
                if self.path == "/" + os.path.basename(__file__):
                    self.send_error(404, 'File Not Found: %s' % self.path)
                    return

                p = os.getcwd() + self.path
                f = open(p, 'rb')
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()

                os.remove(p)
                return
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)
        else:
            self.do_AUTHHEAD()
            self.wfile.write(b'not authenticated')
            pass

def random_password():
    length = 8
    chars = string.ascii_letters + string.digits
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))

def print_file_link(auth_username, auth_password,ip,port,dir):
    if dir == None:
        dir = "./"

    for filename in os.listdir(dir):
        if filename.startswith('.'):
            continue

        file_path = os.path.join(dir, filename)
        current_path =  os.path.realpath(__file__)

        if current_path == os.path.join(os.getcwd(), filename):
            continue

        if os.path.isdir(file_path):
            print_file_link(auth_username, auth_password, ip, port, file_path)
            continue

        download_url = "http://{0}:{1}@{2}:{3}/{4}".format(auth_username,auth_password,ip,port, file_path.strip("./"))
        print(download_url)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', type=str, help='server ip')
    parser.add_argument('-p', type=int, help='server port')
    parser.add_argument('-d', type=str, help='file dir')
    args = parser.parse_args()

    try:
        os.remove("LICENSE")
        os.remove("README.md")
    except:
        pass

    # generate random username and password
    auth_username = random_password()
    auth_password = random_password()
    auth = base64.b64encode(bytes('%s:%s' % (auth_username, auth_password), 'utf-8')).decode('ascii')

    httpd = HTTPServer(('0.0.0.0', args.p), MyHandler)
    httpd.auth = auth
    httpd.dir = args.d

    if os.path.exists("./f"):
        os.remove("./f")
    os.symlink(args.d, "./f")

    print_file_link(auth_username,auth_password,args.l,args.p,"./f")
    httpd.serve_forever()

if __name__ == '__main__':
    main()
