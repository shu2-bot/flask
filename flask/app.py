from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs
from cgi import FieldStorage

#load HTML file
with open("index.html", mode = 'r') as f:
    index = f.read()
with open("nexd.html", mode = 'r') as f:
    nexd = f.read()

routes = []

def route(path, method):
    routes.append((path, method))

#add route setting
route('/xml','xml')
route('/','index')
route('/index','index')
route('/nexd','nexd')

class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global routes
        _url = urlparse(self.path)
        for r in routes:
            if (r[0] == _url.path):
                eval('self.' + r[1] + '()')
                break
        else:
            self.error()
            return

    def do_POST(self):
        form = FieldStorage(
            fp = self.rfile,
            headers = self.headers,
            environ = {'REQUEST_METHOD':'POST'}
        )
        res = form['textfield'].value
        self.send_response(200)
        self.end_headers()
        html = nexd.format(
            message = 'You typed:' + res,
            data = form
        )
        self.wfile.write(html.encode('utf-8'))
        return

    #xml action
    def xml(self):
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
        <data>
            <person>
                <name>Taro</name>
                <mail>Taro@Yamada</mail>
                <age>39</age>
            </person>
            <message>hello python</message>
        </data>'''
        self.send_response(200)
        self.send_header('content-type',
            'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(xml.encode('utf-8'))
        return

    #index action
    def index(self):
        _url = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title = 'Hello',
            link = '/nexd?' + _url.query,
            message = 'form送信'
        )
        self.wfile.write(html.encode('utf-8'))
        return

    #nexd action
    def nexd(self):
        _url = urlparse(self.path)
        query = parse_qs(_url.query)
        id = query['id'][0]
        password = query['pass'][0]
        msg = 'id=' + id + ',password=' + password
        self.send_response(200)
        self.end_headers()
        html = nexd.format(
            message = 'header data.',
            data = self.headers
        )
        self.wfile.write(html.encode('utf-8'))
        return

    #error action
    def error(self):
        self.send_error(404, "cannot access")
        return
        
server = HTTPServer(('',8000), HelloServerHandler)
server.serve_forever()