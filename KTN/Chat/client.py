'''
KTN-project 2013 / 2014
'''
import socket
from MessageWorker import *
import time

class Client(object):

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        self.connection.connect((host, port))

        self.worker = ReceiveMessageWorker(self)
        self.worker.start()

        while True:
            self.send(raw_input())

        self.connection.close()

    def test(self):
        while True:
            data = self.connection.recv(1024).strip()
            if not data:
                break
            else:
                self.message_received(data, self.connection)

    def message_received(self, message, connection):
        print 'Received from server: ' + message

    def connection_closed(self, connection):
        pass

    def send(self, data):
        self.connection.sendall(data)

    def force_disconnect(self):
        self.worker

    def quit(self):
        self.worker.stopped = True
        self.woerk._Thread__stop()

if __name__ == "__main__":
    client = Client()
    client.start('localhost', 9999)
