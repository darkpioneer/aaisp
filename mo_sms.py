#!/usr/bin/python
# AAISP MO SMS Receiver

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi, sys

class PostHandler(BaseHTTPRequestHandler):
	def do_POST(self):
	# Parse the form data posted
		form = cgi.FieldStorage(
			fp=self.rfile, 
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],})

		# Get data from fields as per http://aa.net.uk/kb-telecoms-sms.html
		# scts	The Service Centre Time Stamp in ISO format, which may include time zone. 
		#		Where the original text has a timestamp, this is used and so 
		#		may be incorrect or have an unexpected time zone depending on the original SMSC.
		#
		# oa	The sending number (or name). The format depends on the original text,
		#		and this could be a name, or a number, and could be national or international format.
		#		* This seems to be just the SIM ICCID (Tom)
		#
		# da	The destination number, normally in international number format.
		#		This could have an additional digit (sub address) in some cases where our interconnect allows it. 
		#		The sub address 9 is not normally used.
		#
		# udh	If there is a User Data Header, then the hex for that header.
		#		We concatenate messages where possible (not SIP2SIM MO at present).
		#		Note that in this case any concatenation headers are removed and the final
		#		concatenated message is passed to you, so this will only be otherUDH fields that may be present.
		#
		# ud	The message encoded in UTF-8 format. The special case is where the message contains a null
		#		(e.g. when 8 or 16 bit coding is used and a null included) which is encoded in the invalid UTF-8 sequence 0xC0 0x80.
		#
		# dcs	The Data Coding Scheme (if not 0), in decimal.
		#
		# pid	The Protocol Identifier (if not 0), in decimal.


		timestamp = form.getvalue('scts')
		source = form.getvalue('oa')  
		destination = form.getvalue('da')
		text = form.getvalue('ud')
		header = form.getvalue('udh')
		dcs = form.getvalue('dcs')
		pid = form.getvalue('pid')

		# Begin the response
		self.send_response(200)
		self.end_headers()
		
		# Put own code here for dealing with SMS
		
		# Print the sms received
		print timestamp
		print "SMS Received From ICCID: " + source + " sent to: " + destination + " containing the text: " + text
		print "--------"
    
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
