import SocketServer

class ClientHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        print self.client_address, 'connected!'
        self.request.send('hi ' + str(self.client_address) + '\n')

    def handle(self):
        while 1:
            data = self.request.recv(1024)
            self.request.send(data)
            if data.strip() == '/logout':
                return

    def finish(self):
        print self.client_address, 'disconnected!'
        self.request.send('bye ' + str(self.client_address) + '\n')

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, debug=True):
        self.users = {}
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)


if __name__ == "__main__":
    server = ThreadedTCPServer(('localhost', 9999), ClientHandler)
    server.serve_forever()