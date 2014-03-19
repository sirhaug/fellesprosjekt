#-*- coding: utf-8 -*-
import socket
import threading
from Queue import Queue
import thread
import json
import sysmsg
import re
import time

REQUEST = 'request'
ERROR = 'error'
MESSAGE = 'message'
RESPONSE = 'response'
USERNAME = 'username'
LOGIN = '/login'
LOGOUT = '/logout'


class ClientHandler(threading.Thread):
    def __init__(self, connection, address, pending, connected_clients, logged_users):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.connected_clients = connected_clients
        self.pending = pending
        self.logged_users = logged_users
        self.username = None

    def run(self):
        thread.start_new_thread(self.send, ())
        while True:
            if self.username == '':
                break
            data = self.connection.recv(1024)
            thread.start_new_thread(self.logic, (data,))


    def logic(self, data):
        log_lock = thread.allocate_lock()
        try:
            data = json.loads(data)
        except:
            pass
        rec = data[REQUEST]
        if USERNAME in data:
            user = data[USERNAME]
        else:
            user = self.username
        if rec == LOGIN:
            if not self.testValidName(user):
                self.connection.sendAll(sysmsg.userInvalid(user))
            elif not self.testUniqueness(user, logged_users):
                self.connection.sendOne(sysmsg.userTaken(user))
            #adds user to list of connections and  creates a new thread to listen to
            #incoming messages.
            else:
                print 'success'
                self.sendOne(sysmsg.userOk(user))
                log_lock.acquire()
                self.logged_users.append(user)
                self.connected_clients[connection] = True
                log_lock.release()
                self.username = user
                pending.put(sysmsg.userLoggedIn(user))

        elif rec == LOGOUT:
            if self.checkUser():
                self.sendOne(sysmsg.alreadyLoggedOut(user))
            else:
                log_lock.acquire()
                logged_users.remove(self.username)
                del connected_clients[connection]
                log_lock.release()
                self.username = ''
                self.sendOne(sysmsg.userLogout(user))
                pending.put(sysmsg.userLogout(user))

        elif rec == MESSAGE:
            print 'received'
            if self.checkUser():
                self.sendOne(sysmsg.notLoggedInn(user))
            else:
                print 'put in queue '
                my_string = user + " " + time.asctime().split()[3] + ': ' + data[MESSAGE]
                data[MESSAGE] = my_string
                del data[REQUEST]
                data[RESPONSE] = rec
                data = json.dumps(data)
                pending.put(data)
                print "Messages in queue: "+str(pending.qsize())


    def checkUser(self):
        if self.username == None or self.username == '':
            return True
        else:
            return False

    def testUniqueness(self, name, nameList):
        if name in nameList:
            return False
        else:
            return True

    def testValidName(self, name):
        checked_name = ""
        for i in name:
            checked_name += re.match("[\w]*", i).group()
        if name == checked_name:
            return True
        else:
            return False

    def sendOne(self, message):
        self.connection.sendall(message)

    def send(self):
        while True:
            delete = []
            data = pending.get()

            for i in self.connected_clients:
                try:
                    if self.connected_clients[i] == True:
                        i.sendall(data)
                except socket.error, msg:
                    delete.append(i)
                    print str(i) + ' has disconnected'
            for a_thread in delete:
                del connected_clients[a_thread]
            pending.task_done()
            print "Message sent\nMessages in queue: "+str(pending.qsize())


pending = Queue()
connected_clients = {}
logged_users = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname()
PORT = 8945

s.bind((HOST, PORT))
s.listen(20)
print 'Now waiting for connections...'

while True:
    connection, address = s.accept()
    if connection not in connected_clients:
        connected_clients[connection] = False
        this_thread = ClientHandler(connection, address, pending, connected_clients, logged_users)
        this_thread.start()
        print str(address) + ' just connected'
