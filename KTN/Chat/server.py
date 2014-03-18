'''
KTN-project 2013 / 2014
Very simple server implementation that should serve as a basis
for implementing the chat server
'''
import SocketServer
import re

'''
The RequestHandler class for our server.

It is instantiated once per connection to the server, and must
override the handle() method to implement communication to the
client.
'''


class ClientHandler(SocketServer.BaseRequestHandler):
    def handle(self):
    	def login():
        	# Wait for data from the client
            data = self.connection.recv(1024).strip()
            # Check if the data exists
            # (recv could have returned due to a disconnect)
            if data:
            	# self.user = self.server.login(data)
            	if data.lower() == "/login":
            		self.connection.sendall("Type in your username, only alphanumeric letters and underscores are valid.")
            		self.connection.sendall("WARNING: If you type in more than one continuous word, only the first word will be accepted.")
            		self.connection.sendall("         All non-valid characters will be omitted from your username.")
            		username = re.match('[\w]*', self.connection.recv(1024).strip()).group()

            		if (username != None) and not (self.server.users.has_key(username)):
            			self.user = self.server.login(username)
            			return True
            		else:
            			self.connection.sendall("Invalid username, or username is already taken.")
            	else:
            		self.connection.sendall("Please use '/login' to login")

            	return False

            else:
                disconnect()

        def broadcast(data):
        	self.connection.sendall(data)

        def disconnect():
			self.connection.sendall("Client disconnected!")
			print 'Client disconnected!'

        # Get a reference to the socket object
        self.connection = self.request
        # Get the remote ip adress of the socket
        self.ip = self.client_address[0]
        # Get the remote port number of the socket
        self.port = self.client_address[1]
        print 'Client connected @' + self.ip + ':' + str(self.port)
        
        while True:
        	flag = login()
        	if flag:
        		break

        while True:
            # Wait for data from the client
            data = self.connection.recv(1024).strip()
            # Check if the data exists
            # (recv could have returned due to a disconnect)
            if data:
            	# self.user = self.server.login(data)
            	if data.lower() == "/login":
            		self.connection.sendall("You are already logged in.")
                
                elif data.lower() == "/logout":
                	self.server.logout()

               	else:
               		broadcast(data)

            else:
                disconnect()
                break    

'''
This will make all Request handlers being called in its own thread.
Very important, otherwise only one client will be served at a time
'''
class User():

    def __init__(self, username):
        self.username = username

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, debug=True):
        self.users = {"martin":User("martin")}
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)

    def login(self, username):
        print "login: " + username
        self.users[username] = User(username)
        #return self.users[-1]

    def logout(self):
    	users.pop(self.username)


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 9999

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
