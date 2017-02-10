'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.


'''

import signal
import sys
import ssl
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from optparse import OptionParser

import select
import socket
import argparse
import logging
import serial
import sys
import time
import threading
import myweb


s_handle = serial.Serial(port='COM1',baudrate=9600,timeout = 0.1)

clients = []

class foward_serial(WebSocket):
    global s_handle
    def handleMessage(self):
        for client in clients:
            print 'handle message ...'
            try:
                print 'write data:' + self.data
                print 'len:' + str(len(self.data))
                s_handle.write(str(self.data))           
                ser_output = s_handle.read(1024)
                print 'read data:' + ser_output            
                print 'handle message ...4'
                client.sendMessage(ser_output)
            except Exception as e:
                print 'exception:' + str(e)
    def handleConnected(self):
        try:
            print (self.address, 'connected')
            for client in clients:
                client.sendMessage(self.address[0] + u' - connected')
            clients.append(self)
        except Exception as e:
            print 'exception:' + str(e)

    def handleClose(self):
        try:
            if self in clients:
                clients.remove(self)
                print (self.address, 'closed')
                for client in clients:
                    client.sendMessage(self.address[0] + u' - disconnected')         
        except Exception as e:
            print 'exception:' + str(e)
if __name__ == "__main__":

   threading.Thread(target=myweb.my_web_server).start()
   
   parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
   parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
   parser.add_option("--port", default=8000, type='int', action="store", dest="port", help="port (8000)")
   parser.add_option("--example", default='echo', type='string', action="store", dest="example", help="echo, chat")
   parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
   parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
   parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

   (options, args) = parser.parse_args()

   #cls = SimpleEcho
   #if options.example == 'chat':
   cls = foward_serial

   if options.ssl == 1:
      server = SimpleSSLWebSocketServer(options.host, options.port, cls, options.cert, options.cert, version=options.ver)
   else:
      server = SimpleWebSocketServer(options.host, options.port, cls)

   def close_sig_handler(signal, frame):
      server.close()
      sys.exit()

   signal.signal(signal.SIGINT, close_sig_handler)

   server.serveforever()
