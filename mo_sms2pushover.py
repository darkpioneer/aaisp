#!/usr/bin/python
# AAISP sip2sim MO SMS Pushover gateway
# Recives MO SMS data from sip2sim and passes it to pushover

# Pushover Settings
APP_TOKEN = "APP TOKEN"
USER_KEY = "USER KEY"
#

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi, sys, httplib, urllib
conn = httplib.HTTPSConnection("api.pushover.net:443")

class PostHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self._set_headers()
		self.wfile.write("<html><body><h1>MO GATEWAY</h1></body></html>")
	def do_POST(self):
	# Parse the form data posted
		form = cgi.FieldStorage(
			fp=self.rfile, 
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
					'CONTENT_TYPE':self.headers['Content-Type'],
					})

		# Get data from fields
		timestamp = form.getvalue('scts')
		source = form.getvalue('oa')  
		destination = form.getvalue('da')
		text = form.getvalue('ud')
		header = form.getvalue('udh')
		dcs = form.getvalue('dcs')
		pid = form.getvalue('pid')

		# Begin the response
		self.send_response(200) #  Send HTTP 200 (OK) back to AAISP or phone reports "SMSService Rejected Message(71:ERR)"
		self.end_headers()

		print "SMS Received From ICCID: " + source + " sent to: " + destination + " containing the text: " + text
		print "sending to pushover"
		conn.request("POST", "/1/messages.json",
			urllib.urlencode({
				"token": APP_TOKEN,
				"user": USER_KEY,
				"title": source,
				"message": text,
			}), { "Content-type": "application/x-www-form-urlencoded" })
		response = conn.getresponse()
		print response.status, response.reason
		print response.read()
		conn.close()

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