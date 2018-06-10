import socket
import StringIO
import sys

class WGIServer(object):
	address_family = socket.AF_INET
	socket_type = socket.SOCK_STREAM
	request_queue_size = 1

	def __init__(self, server_address):
		#create a listening socket
		self.listen_socket = listen_socket = socket.socket(self.address_family, self.socket_type)
		#allow reuse of same address
		listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#bind
		listen_socket.bind(server_address)
		#activate
		listen_socket.listen(self.request_queue_size)
		#get server host name and port
		host, port = self.listen_socket.getsockname()[:2]
		self.server_name = socket.getfqdn(host)
		self.server_port = port
		#return headers set by web framework/application
		self.headers_set = []

	def set_app(self, application):
		self.application = application

	def serve_forever(self):
		listen_socket = self.listen_socket
		while True:
			#new client connection
			self.client_connection, client_address = listen_socket.accept()
			#handle one request and close the connection. Then loop over to wait for another client connection
			self.handle_one_request()
	
	def handle_one_request():
		self.request_data = request_data = self.client_connection.recv(1024)
		#print formatted request data a la 'curl -v'
		print(''.join(
		      '< {line}\n'.format(line=line)
		      for line in request_data.splitlines()
	        ))

		self.parse_request(request_data)

		#construct env dict using request data
		env = self.get_environ()

		#call application callable and get back result that will become HTTP response body
		result = self.application(env, self.start_response)
		
		#construct response and send back to client
		self.finish_response(result)
	
	def parse_request(self, text):
		request_line = text.splitlines()[0]
		request_line = request_line.rstrip('\r\n')
		#break down request line into components
		(self.request_method, self.path, self.request_version) = request_line.split()

	def get_environ(self):
		env = {}
		#required wsgi variables
		env['wsgi.version'] = (1, 0)
		env['wsgi.url_scheme'] = 'http'
		env['wsgi.input'] = StringIO.StringIO(self.request_data)
		env['wsgi.errors'] = sys.stderr
		env['wsgi.multithread'] = False
		env['wsgi.multiprocess'] = False
		env['wsgi.run_once'] = False
		#required cgi variables
		env['REQUEST_METHOD'] = self.request_method
  		env['PATH_INFO'] = self.path
		env['SERVER_NAME'] = self.server_name
		env['SERVER_PORT'] = str(self.server_port)
		return env

	def start_response(self, status, response_headers, exc_info=None):
		# add necessary server headers
		server_headers = [ 
		    ('Date', 'Sun, 10 June 2018 12:00:00 GMT'),
		    ('Server', 'WSGIServer 0.2'),
		]
		self.headers_set = [status, response_headers + server_headers]

	def finish_response(self, result)
		try:
			status, response_headers = self.headers_set
			response = 'HTTP/1.1 {status}\r\n'.format(status=status)
			for header in response_headers:
				response += '{0}: {1}\r\n'.format(*header)
			response += '\r\n'
			for data in result:
				response += data
			print(''.join(
			      '> {line}\n'.format(line=line)
			      for line in response.splitlines()
			))
			self.client_connection.sendall(response)
		finally:
			self.client_connection.close()
	
	SERVER_ADDRESS = (HOST, PORT) = '', 8888
	
	def make_server(server_address, application):
		server = WSGI(server_address)
		server.set_app(application)
		return server

	if __name__ == '__main__':
		if len(sys.argv) < 2:
			sys.exit('Provide a WSGI application object as module:callable')
		app_path = sys.argv[1]
		module, application = app_path.split(':')
		module = __import__(module)
		application = getattr(module, application)
		httpd = make_server(SERVER_ADDRESS, application)
		print('WSGIServer: Serving HTTP on port {port} ... \n'.format(port=PORT))
		httpd.server_forever()
