'''
KTN-project 2013 / 2014
Very simple server implementation that should serve as a basis
for implementing the chat server
'''
import SocketServer

'''
The RequestHandler class for our server.

It is instantiated once per connection to the server, and must
override the handle() method to implement communication to the
client.
'''


class ClientHandler(SocketServer.BaseRequestHandler):
    def handle(self):

        # Get a reference to the socket object
        self.connection = self.request
        # Get the remote ip adress of the socket
        self.ip = self.client_address[0]
        # Get the remote port number of the socket
        self.port = self.client_address[1]
        print 'Client connected @' + self.ip + ':' + str(self.port)
        
        while True:
            # Wait for data from the client
            data = self.connection.recv(1024).strip()
            # Check if the data exists
            # (recv could have returned due to a disconnect)
            if data:
                # self.user = self.server.login(data)
                print data
                # Return the string in uppercase
                self.connection.sendall(data.upper())

            else:
                disconnect()
                break

        def disconnect():
            print 'Client disconnected!'
            

'''
This will make all Request handlers being called in its own thread.
Very important, otherwise only one client will be served at a time
'''
class User():

    def __init__(self, username):
        self.username = username

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, debug=True):
        self.users = [User("martin")]
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)

    def login(self, username):
        print "login: " + username
        return self.users[0]

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 9999

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
