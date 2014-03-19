#-*- coding: utf-8 -*-
from Queue import Queue
import json
import re
import socket
import sysmsg
import thread
import threading
import time

REQUEST = 'request'
ERROR = 'error'
MESSAGE = 'message'
RESPONSE = 'response'
USERNAME = 'username'
LOGIN = '/login'
LOGOUT = '/logout'


class ClientHandler(threading.Thread):
    def __init__(self, connection, address, pending, connected_clients):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.pending = pending
        self.connected_clients = connected_clients
        self.username = None

    def run(self):
        thread.start_new_thread(self.send, ())
        while True:
            if self.username == "":
                break
            data = self.connection.recv(1024)
            thread.start_new_thread(self.process, (data,))

    def process(self, data):
        process_lock = thread.allocate_lock()

        try:
            json.loads(data)
        except:
            pass

        if [USERNAME] in data:
            user = data[USERNAME]
        else:
            user = self.username

        #Handle requests
        request = data[REQUEST]
        if request == LOGIN:
            #Assuring that two threads doesn't try
            #appending the same username at the same time
            process_lock.aquire()
            if self.invalidName(user):
                self.connection.sendall(sysmsg.invalidUser(user))
            elif self.notUniqueName():
                self.connection.sendall(sysmsg.nameTaken(user))
            else:
                self.connection.sendall(sysmsg.userIsAllGood(user))
                self.connected_clients[user] = self.connection
                self.username = user
                pending.put(sysmsg.userLogin(user))
            process_lock.release()

        elif request == LOGOUT:
            if not self.isLoggedIn(self.connected_clients):
                self.connection.sendall(sysmsg.alreadyLoggedOut(user))
            else:
                process_lock.aquire()
                del connected_clients[self.username]
                process_lock.release()
                self.username = ''
                self.connection.sendall(sysmsg.userLogout(user))
                pending.put(sysmsg.userLogout(user))

        elif request == MESSAGE:
            print "Message recieved"
            if not self.isLoggedIn(self.connected_clients):
                self.connection.sendall(sysmsg.notLoggedIn(user))
            else:
                data[MESSAGE] = user + " said @ " + time.asctime().split()[3] + "\n" + data[MESSAGE]
                del data[REQUEST]
                data[RESPONSE] = request
                data = json.dumps(data)
                pending.put(data)
                print "Messages in queue: " + str(pending.qsize())

    def isLoggedIn(self, connected_clients):
        return self.username in connected_clients

    def notUniqueName(self):
        return self.isLoggedIn()

    def invalidName(self, username):
        checked_name = ""
        for i in username:
            checked_name += re.match("[\w]*", i).group()
        if username == checked_name:
            return False
        else:
            return True

    def send(self):
        while True:
            delete = []
            data = pending.get()
            sender = data[USERNAME]
            del data[USERNAME]

            for user in self.connected_clients:
                try:
                    if user != sender:
                        self.connected_clients[user].sendall(data)
                except socket.error:
                    delete.append(user)
                    print str(connected_clients[user]) + " fell of the railway..."

            for user in delete:
                del connected_clients[user]
            pending.task_done()
        print "Message sent\nMessages in queue: " + str(pending.qsize())


pending = Queue()
connected_clients = {}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname()
PORT = 8945

sock.bind((HOST, PORT))
sock.listen(20)
print "Now waiting for connections..."

while True:
    connection, address = sock.accept()
    if connection not in connected_clients:
        this_thread = ClientHandler(connection, address, pending, connected_clients)
        this_thread.start()
        print str(address) + " just connected"