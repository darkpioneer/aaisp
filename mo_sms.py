#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi, sys

class PostHandler(BaseHTTPRequestHandler):
	def do_POST(self):
	# Parse the form data posted
		form = cgi.FieldStorage(
			fp=self.rfile, 
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],})

		# Get data from fields, posted values from https://support.aa.net.uk/SMS_API
		username = form.getvalue('username')
		password = form.getvalue('password')
		source = form.getvalue('oa')  
		destination = form.getvalue('da')
		text = form.getvalue('ud')
		limit = form.getvalue('limit')
		costcentre = form.getvalue('costcentre')
		private = form.getvalue('private')
		udh = form.getvalue('udh')
		srr = form.getvalue('srr')

		# Begin the response
		self.send_response(200)
		self.end_headers()
		
		# Print the sms received
		print "SMS Received From ICCID: " + source + " sent to: " + destination + " containing the text: " + text
    
def run(server_class=HTTPServer, handler_class=PostHandler, port=8001):
	try:
		server_address = ('', port)
		httpd = server_class(server_address, handler_class)
		print 'Starting server, use <Ctrl-C> to stop'
		httpd.serve_forever()
	except KeyboardInterrupt:
		print "Shutting Down"
	except Exception:
		trackback.print_exc(file=sys.stdout)
	sys.exit(0)

if __name__ == "__main__":
	from sys import argv

	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()
