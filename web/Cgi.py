import logging
from os import getcwd
from flask import request, render_template, jsonify
from flask_socketio import emit

class CgiSocket(object):
    def __init__(self):
        self.events = {'publish-sensors':self.sensors,'publish-actions':self.actions}
        self.args = {'emitter':None,'namespace':'default','listen':False}
        self.namespace = 'default'
        self.emitter = None

    def decorate(self,arguments):
        from Process import decorate
        return decorate(self,arguments)

    def create(self,socket):
        self.emitter = self.args.get('emitter')
        if None == self.emitter:
            logging.error('no event dispatcher set')
            return self
        self.external = socket
        self.namespace = self.args.get('namespace')
        self.external.on('connect',namespace='/%s'%self.namespace)(self.connect) # == @socketio.on('connect',namespace='/namespace')
        self.external.on('request',namespace='/%s'%self.namespace)(self.request) # == @socketio.on('request',namespace='/namespace')
        self.external.on('disconnect',namespace='/%s'%self.namespace)(self.disconnect) # == @socketio.on('disconnect',namespace='/namespace')
        self.external.on('error',namespace='/%s'%self.namespace)(self.error) # == @socketio.on_error(/namespace')
        logging.info('%s socket created'%self.namespace)
        return self

    def connect(self):
        logging.info('connect-%s'%self.namespace)
        self.external.emit('connected', {'call':'%s-connected'%self.namespace,'id':'connect-%s'%self.namespace},namespace='/%s'%self.namespace) 

    def request(self,data):
        logging.debug('request-%s'%self.namespace)
        data['call'] = data['request']
        data['host'] = request.host #    print dir(request)
        data['sid'] = request.sid
        self.external.emit('response', {'call':'%s-request'%self.namespace,'id':'response-%s'%self.namespace,'origin':data},namespace='/%s'%self.namespace) 

    def disconnect(self):
        logging.info('%s disconnected from %s'%(request.host,self.namespace))

    def error(self,error):
        logging.error('cameras error %s'%str(e))

    def sensors(self,data):
        if self.args.get('listen'):
            self.external.emit('response', {'call':'%s-sensors'%self.namespace,'id':'response-%s'%self.namespace,'sensors':data},namespace='/%s'%self.namespace) 

    def actions(self,data):
        if self.args.get('listen'):
            self.external.emit('response', {'call':'%s-actions'%self.namespace,'id':'response-%s'%self.namespace,'actions':data},namespace='/%s'%self.namespace) 

class CgiErrors(object):
    def __init__(self):
        self.args = {'path':'errors','errors':[]}
        # unsupported 101,102,103,200,201,202,203,204,205,206,207,208,226,300,301,302,303,304,305,306,307,308,402,407,418,421,422,423,424,426,506,507,508,510,511
        self.errors = [400,401,403,404,405,406,408,409,410,411,412,413,414,415,416,417,428,429,431,451,500,501,502,503,504,505]
    def decorate(self,arguments):
        keys = self.args.keys()
        for key in arguments:
            if key in keys:
                self.args[key] = arguments[key]
        return self

    def create(self,cgi):
        custom = self.args.get('errors')
        for code in custom:
            cgi.register_error_handler(int(code),self.handler)
        for code in self.errors:
            if not code in custom:
                cgi.register_error_handler(int(code),self.default)

    def default(self,error):
        if hasattr(error, 'errno'): # flask_login.login_required fail
            return render_template('%s/500.html'%(self.args.get('path'),500)),500
        else:
            return render_template('%s/default.html'%self.args.get('path'),code=error.code,name=error.name,description=error.description,message=error.message,args=error.args,response=error.response),error.code

    def handler(self,error):
        if hasattr(error, 'errno'): # flask_login.login_required fail error.name = template
            return render_template('%s/500.html'%self.args.get('path')),500
        else: # flask
            return render_template('%s/%s.html'%(self.args.get('path'),error.code)),error.code

class CgiRoutes(object):
    def __init__(self):
        self.args = {'index':'index.html','path':'pages'}
        self.routes = {'/':self.index}
        self.path = None
        self.index = None

    def decorate(self,arguments):
        from Process import decorate
        return decorate(self,arguments)

    def create(self,cgi):
        for key in self.routes.keys():
            cgi.add_url_rule(key,view_func=self.routes.get(key))
        self.index = '%s/%s'%(self.args.get('path'),self.args.get('index'))

    def index(self):
        return render_template(self.index,title='muK.1nd3x'),200

class CgiWatchdogs(object):
    def __init__(self):
        self.args = {'watchdogs':[]}
        self.watchdogs = {'custom':self.custom,'firebase':self.firebase}

    def decorate(self,arguments):
        keys = self.args.keys()
        for key in arguments:
            if key in keys:
                self.args[key] = arguments[key]
        return self

    def create(self):
        dogs = self.watchdogs.keys()
        for dog in self.args.get('watchdogs'):
            if dog in dogs():
                self.watchdogs(dog)

    def custom(self):
        def custom_login_required(f):
            from functools import wraps
            @wraps(f)
            def decorated_function(*args, **kwargs):
                print '----------------------------'
                print 'check if custom is logged in'
                print '----------------------------'
            #    if g.user is None:
            #        return redirect(url_for('login', next=request.url))
                return f(*args, **kwargs)
            return decorated_function

    def firebase(self):
        def firebase_login_required(f):
            from functools import wraps
            @wraps(f)
            def decorated_function(*args, **kwargs):
                print '------------------------------'
                print 'check if firebase is logged in'
                print '------------------------------'
            #    if g.user is None:
            #        return redirect(url_for('login', next=request.url))
                return f(*args, **kwargs)
            return decorated_function

class Cgi(object):
    def __init__(self,folder='%s/static'%getcwd()):
        self.events = {'push-sio':self.push,'start-monitor':self.create,'monitor-options':self.decorate}
        self.args = {'emitter':None,'host':'0.0.0.0','port':5000,'logger':None,'debug':False,'deamon':True
                    ,'key':'ssl/host.key','crt':'ssl/host.crt'}
        from flask import Flask
        self.cgi = Flask(__name__,template_folder=folder,static_folder=folder)
        from flask_socketio import SocketIO
                                                                                             # async_mode eventlet|gevent|threading
        self.socket = SocketIO(self.cgi,async_mode='threading',debug=self.args.get('debug')) # eventlet is best performance, but threading works
        self.socket.on_error_default(self.error) # == @socketio.on_error_default | socketio.on_error(None)(handler)
        from flask_login import LoginManager
        self.login = LoginManager(self.cgi)
        self.login.login_view = 'login' # == url_for(login) # name of the function
        from glob import glob
        path = '%s/static/pages/'%getcwd()
        pages = glob('%s*.html'%path)
        for i, page in enumerate(pages):
            pages[i] = page.replace(path,'').replace('.html','')
        print pages
        CgiRoutes().decorate({'index':'4Dm1n.html'}).create(self.cgi)
        path = '%s/static/errors/'%getcwd()
        pages = glob('%s[1-5][0-9][0-9].html'%path)
        for i, page in enumerate(pages):
            pages[i] = int(page.replace(path,'').replace('.html',''))
        print pages
        CgiErrors().decorate({'errors':pages}).create(self.cgi)

    def decorate(self,arguments):
        from Process import decorate
        return decorate(self,arguments)

    def create(self,data={}):
        self.cgi.config['HOST'] = self.args.get('host')
        self.cgi.config['PORT'] = self.args.get('port')
        self.cgi.config['DEBUG'] = self.args.get('debug')
        if not None == self.args.get('logger'):
            # self.cgi.logger = self.args.get('logger') # error can't set attribute
            if(0 < len(self.cgi.logger.handlers)):
                self.cgi.logger.handlers.pop()
            self.cgi.logger.addHandler(self.args.get('logger'))
        from threading import Thread
        self.thread = Thread(target=self.start)
        self.thread.setDaemon(self.args.get('deamon'))
        self.thread.start()
        return self

    def start(self):
        self.cgi.run(ssl_context=(self.args.get('crt'),self.args.get('key')))
        return self

    def error(self,error):
        logging.error('default socket error %s'%str(error))

    def push(self,data):
        namespace = data.get('namespace')
        self.socket.emit('response',{'call':'%s-got'%namespace,'id':'push-%s'%namespace,'data':data},namespace='/%s'%namespace)
