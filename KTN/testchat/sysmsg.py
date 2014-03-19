#-*- coding: utf-8 -*-
import json

REQUEST = 'request'
ERROR = 'error'
MESSAGE = 'message'
RESPONSE = 'response'
USERNAME = 'username'
LOGIN = '/login'
LOGOUT = '/logout'


def userOk(name):
    ourDict = {RESPONSE: LOGIN, USERNAME: name, 'messages': ''}
    return json.dumps(ourDict)


def userLoggedIn(name):
    ourDict = {RESPONSE: MESSAGE, MESSAGE: name + ': just logged in'}
    return json.dumps(ourDict)


def userInvalid(name):
    ourDict = {RESPONSE: LOGIN, ERROR: 'Invalid username!', USERNAME: name}
    return json.dumps(ourDict)


def userTaken(name):
    ourDict = {RESPONSE: LOGIN, ERROR: 'Name already taken!', USERNAME: name}
    return json.dumps(ourDict)


def userLogout(name):
    ourDict = {RESPONSE: LOGOUT, USERNAME: name + ': just logged out'}
    return json.dumps(ourDict)


def alreadyLoggedOut(name):
    ourDict = {RESPONSE: LOGOUT, ERROR: 'You just logged out!', USERNAME: name}
    return json.dumps(ourDict)


def notLoggedInn(name):
    ourDict = {RESPONSE: MESSAGE, ERROR: 'You are not logged in!'}
    return json.dumps(ourDict)

