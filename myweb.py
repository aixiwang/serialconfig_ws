#-*- coding:utf-8 -*-
import BaseHTTPServer


    
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    
    def do_GET(self):
        f =  open('index.html','r')            
        page = f.read()
    
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

#----------------------------------------------------------------------

def my_web_server():
    serverAddress = ('', 80)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()