#-*- coding: utf-8 -*-
import socket
import thread
import time
import traceback
import json
import sys

REQUEST = 'request'
ERROR = 'error'
MESSAGE = 'message'
RESPONSE = 'response'
USERNAME = 'username'
LOGIN = '/login'
LOGOUT = '/logout'


class Client(object):
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self, host, port):
        self.username = None
        self.print_lock = thread.allocate_lock()
        self.connection.connect((host, port))
        print 'connecting to server'
        thread.start_new_thread(self.message_received, ())
        while True:
            data = raw_input()
            for i in data:
                if i == '[æ-åÆ-Å]':
                    print 'fail'
                    continue
            if self.username == '' or data == '':
                break
            if data == 'u':
                print self.username
            if data == LOGIN:
                print 'Please submit a username: '
                requestUser = raw_input()
                data_dict = {REQUEST: data, USERNAME: requestUser}
            elif data == LOGOUT:
                data_dict = {REQUEST: data}
            else:
                data_dict = {REQUEST: MESSAGE, MESSAGE: data, USERNAME: self.username}
            self.send(json.dumps(data_dict))


    def message_received(self):
        while True:
            data = self.connection.recv(4096)
            try:
                data = json.loads(data)
            except ValueError:
                if data == '':
                    print 'Could not connect to the server.'

                else:
                    print 'We are sorry, an unknown error occurred'
                self.username = ''
                print 'Press enter to exit the program'
                break
            try:
                res = data[RESPONSE]
                if ERROR in data:
                    print data[ERROR]
                    print ""
                elif res == LOGIN:
                    self.username = data[USERNAME]
                elif res == LOGOUT:
                    print data[USERNAME]
                    print ""
                    self.username = ''
                else:
                    print data[MESSAGE]
                    print ""
            except TypeError:
                pass
            except Exception:
                print "Other Exception"
                traceback.print_exc()
                pass


    def connection_closed(self, connection):
        pass

    def send(self, data):
        print 'send'
        self.connection.sendall(data)

    def force_disconnect(self):
        self.connection.close()


if __name__ == "__main__":
    client = Client()
    client.start(socket.gethostname(), 8945)