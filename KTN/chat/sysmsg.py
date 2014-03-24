#-*- coding: utf-8 -*-
import json

REQUEST = "request"
ERROR = "error"
MESSAGE = "message"
RESPONSE = "response"
USERNAME = "username"
LOGIN = "/login"
LOGOUT = "/logout"
BACKLOG = "/backlog"


def userIsAllGood(name):
    jsonBundle = {RESPONSE: LOGIN, USERNAME: name, "messages": ""}
    return json.dumps(jsonBundle)


def userLogin(name):
    jsonBundle = {RESPONSE: MESSAGE, MESSAGE: name + ": just logged in"}
    return json.dumps(jsonBundle)


def invalidUser(name):
    jsonBundle = {RESPONSE: LOGIN, ERROR: "Invalid username!", USERNAME: name}
    return json.dumps(jsonBundle)


def nameTaken(name):
    jsonBundle = {RESPONSE: LOGIN, ERROR: "Name already taken!", USERNAME: name}
    return json.dumps(jsonBundle)


def userLogout(name):
    jsonBundle = {RESPONSE: LOGOUT, USERNAME: name + ": just logged out"}
    return json.dumps(jsonBundle)


def alreadyLoggedOut(name):
    jsonBundle = {RESPONSE: LOGOUT, ERROR: "You just logged out!", USERNAME: name}
    return json.dumps(jsonBundle)


def notLoggedIn():
    jsonBundle = {RESPONSE: MESSAGE, ERROR: "Please use '/login' to login"}
    return json.dumps(jsonBundle)

def sendBacklog(backlog):
    jsonBundle = {RESPONSE: BACKLOG, BACKLOG: backlog}
    return json.dumps(jsonBundle)

