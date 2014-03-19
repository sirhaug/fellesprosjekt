#-*- coding: utf-8 -*-
import json
import socket
import thread
import traceback

REQUEST = 'request'
REQUESTUSERNAME = "/u"
ERROR = 'error'
MESSAGE = 'message'
RESPONSE = 'response'
USERNAME = 'username'
LOGIN = '/login'
LOGOUT = '/logout'
SENDER = 'sender'


class Client(object):
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_lock = thread.allocate_lock()
        self.username = None

    def start(self, HOST, PORT):
        self.connection.connect((HOST, PORT))

        print "Connecting to server..."
        thread.start_new_thread(self.receive_messages, ())

        while True:
            data = raw_input()
            if self.username == "" or data == "":
                break
            if data == REQUESTUSERNAME:
                print self.username
            if data == LOGIN:
                if self.username is None:
                    requestedUsername = raw_input("Please enter desired username: ")
                    data_dict = {REQUEST: data, USERNAME: requestedUsername}
                else:
                    print "You are already logged in as [" + self.username + "]"
                    continue
            elif data == LOGOUT:
                data_dict = {REQUEST: data}
            else:
                data_dict = {REQUEST: MESSAGE, MESSAGE: data}
            data_dict[SENDER] = self.username
            self.connection.sendall(json.dumps(data_dict))

    def receive_messages(self):
        while True:
            data = self.connection.recv(4096)
            try:
                data = json.loads(data)
            except ValueError:
                if data == "":
                    print "Connection error"
                else:
                    print "An error occurred, and we think it has something to do with our hamster-powered servers..."
                self.username = ""
                print "Press enter to exit"
                break
            try:
                response = data[RESPONSE]
                if ERROR in data:
                    print data[ERROR]
                elif response == LOGIN:
                    self.username = data[USERNAME]
                elif response == LOGOUT:
                    print "You [" + data[USERNAME] + "] have logged out"
                    print "---"
                    self.username = ""
                else:
                    print data[MESSAGE]
            except TypeError:
                pass
            except Exception:
                print "Other Exception"
                traceback.print_exc()
                pass


if __name__ == '__main__':
    HOST = socket.gethostname()
    PORT = 8945

    client = Client()
    client.start(HOST, PORT)