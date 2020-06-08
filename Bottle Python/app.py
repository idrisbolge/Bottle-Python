#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from Crypto.Random import get_random_bytes
from bottle import *
from ControlLogin import *
import os
import uuid
import datetime
from script import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

class SSLWSGIRefServer(ServerAdapter):
    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        import ssl
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.socket = ssl.wrap_socket (
         srv.socket,
         certfile='server.pem',  # path to certificate
         server_side=True)
        srv.serve_forever()

# def getSessionId():
#     uid = uuid.UUID(bytes=get_random_bytes(16))
#     return uid.hex

secretKey ="DJAKSGJHASVHAVSHDVAHSDVHASBHJASVJAHVHSFVAUFDVAYUHSFVHASV"#getSessionId()

def require_uid(fn):
    def check_uid(**kwargs):
        if request.get_cookie("USER", secret=secretKey):
            return fn(**kwargs)
        else:
            redirect("/login")
    return check_uid

@route('/static/<filepath:path>')
def send_css(filepath):
    return static_file(filepath, root=os.path.join(ROOT_PATH, 'static'))


@hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@route('/ModemStats/api', method=['OPTIONS', 'GET'])
def MdmSApi():
    response.headers['Content-Type'] = 'application/json'
    return {'ModemStats': ModemStats}

@route('/')
def serve_homepage():
    return template('templates/login.html', msg='')


@post('/login')
def do_login():
    global user
    user = request.forms.get('usr')
    password = request.forms.get('psw')
    if check_Login(user, password):
        Login(secretKey, user, datetime.datetime.now())
        response.set_cookie(name='USER',value=user, secret=secretKey)
        return redirect('/main')
    else:
        redirect('/login')


@route('/login')
def lgn():
    return template("templates/login.html", msg='Hatalı Giriş Yaptınız. Lütfen Tekrar deneyiniz. ')



@route('/main')
@require_uid
def main():
    us = get_role(username = user)
    if us == 'root':
        return template("templates/SetModemParameter.html",role = us, usermsg = user)
    elif us == 'user':
        return template("templates/MeterMenu.html", role = us, usermsg = user)
    elif us == 'test':
        return template("templates/ModemTest.html", role = us, usermsg = user)
    # return template("templates/main-root.html",role = us,usermsg=user, snc=ethIP() )


@post("/logout")
@require_uid
def logout():
    Logout(username=user, LogoutTime=datetime.datetime.now())
    response.delete_cookie(key='USER')
    return redirect('/')


@route("/SetModemParameter")
@require_uid
def SetModemParameter():
    us = get_role(username= user)
    if us == 'root':
        return template('templates/SetModemParameter.html',role = us, usermsg = user)
    else:
        return redirect("/Error")

@route("/MeterMenu")
@require_uid
def MeterMenu():
    us = get_role(username = user)
    if us == 'root' or us == 'user':
        return template('templates/MeterMenu.html',role = us, usermsg = user)
    else:
        return redirect('/Error')

@route("/ModemStats")
@require_uid
def ModemStatsPage():
    # us = get_role(username = user)
    # if us == 'root' or us == 'user':
    #     return template('templates/ModemStats.html',role = us, usermsg = user)
    # else:
    #     return redirect('/Error')
    return template('templates/ModemStats.html',role = "root", usermsg = user)
@route("/ModemTest")
@require_uid
def ModemTest():
    us = get_role(username = user)
    if us == 'root' or us == 'user' or us == 'test':
        return template('templates/ModemTest.html',role = us, usermsg = user)
    else:
        return redirect('/Error')








run(host='localhost', debug=True, reloader=True, port=8080)
# srv = SSLWSGIRefServer(host='localhost', port=8080)
# run(server=srv)

