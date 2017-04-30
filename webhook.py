
import os
import subprocess
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import socket

PORT_NUMBER = 4567

class myHandler(BaseHTTPRequestHandler):
        def do_GET(self):
                if( len(self.path.split('?')) < 2):
                        self.send_response(404)
                fullrequest = self.path.split('?')[1].split('&')[0]
                request = ""
                value = ""
                if( len(fullrequest.split('=')) < 2):
                        request = fullrequest
                else:
                        request = fullrequest.split('=')[0]
                        value = fullrequest.split('=')[1]

                if request == "ring":
			open("ring", 'w')
			self.send_response(200)
                else:
                        print "Unknown request: ", request


if __name__ == '__main__':
	try:
		server = HTTPServer(("",PORT_NUMBER),myHandler)
		print 'Started Server on port ', PORT_NUMBER
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()
	
