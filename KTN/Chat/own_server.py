import socket
import threading
import re

class ClientHandler(threading.Thread):
    def __init__(self, connection, address, existing_connections, existing_users):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.existing_connections = existing_connections
        self.existing_users = existing_users
        self.username = None

        '''
        def run(self):
            thread.start_new_thread(self)
            while True:
                if self.username == '':
                    break
                data = self.conn.recv(1024)
                thread.start_new_thread(self.logic, (data,))
        '''

'''
Skal kjøres uansett, ikke bare når server startes som main
[if __name__ == '__main__'] er derfor ikke nødvendig
'''
existing_connections = {}
existing_users = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname()
PORT = 4242

sock.bind((HOST, PORT))
sock.listen(20)
print 'server is now listening'

while True:
    connection, address = sock.accept()

    if connection not in existing_connections:
        existing_connections[connection] = False
        client = ClientHandler(connection, address, existing_connections, existing_users)
        client.start()
    print str(address) + ' just connected'