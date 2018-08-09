import logging

def decorate(clazz,arguments):
    keys = clazz.args.keys()
    for key in arguments:
        if key in keys:
            clazz.args[key] = arguments.get(key)
    return clazz

class ProcessDispatcher(object):
    def __init__(self):
        self.events = {}
        self.args = {'trace':False}
    
    def decorate(self,arguments):
        return decorate(self,arguments)

    def attach(self,evts):
        keys = self.events.keys()
        for key in evts.keys():
            if not key in keys:
                self.events[key] = []
            self.events[key].append(evts.get(key))
        return self

    def emits(self,evts):
        for evt in evts:
            self.emit(evt.get('id'),evt)
        return self

    def emit(self,call,data):
        evtIds = self.events.keys();
        if call in evtIds:
            try:
                for evt in self.events.get(call):
                    evt(data)
            except Exception as e:
                if self.args.get('trace'):
                    logging.exception("emit error! %s not reachable due to %s"%(call,e))
                else:
                    logging.error("emit error! %s not reachable due to %s"%(call,e))
        else:
            logging.debug('%s event not found. known events are %s'%(call,', '.join(evtIds)))
        return self

class ProcessLogger(object):
    def __init__(self):
        # log levels
            # CRITICAL  50
            # ERROR     40
            # WARNING   30
            # INFO      20
            # DEBUG     10
            # NOTSET     0
        self.events = {'logger-options':self.decorate}
        self.args = {'path':'unset','level':20,'newfile':True,'shell':True
                    ,'format':'%(asctime)18s %(levelname)7s >> %(process)6s %(module)s.%(funcName)s():%(lineno)d >> %(message)s'
                    ,'date':'%Y-%m-%d %H:%M:%S'}
        self.logger = logging.getLogger()
        self.file = None
        self.shell = None

    def decorate(self,arguments):
        return decorate(self,arguments)

    def create(self,dispatcher=None):
        if dispatcher:
            dispatcher.attach(self.events)
        self.logger.setLevel(self.args.get('level'))
        if(self.logger.handlers):
            self.logger.handlers.pop()
        formatter = logging.Formatter(fmt=self.args.get('format'),datefmt=self.args.get('date'))
        if(self.args.get('shell')):
            import sys
            self.shell = logging.StreamHandler(sys.stdout)
            self.shell.setFormatter(formatter)
            self.logger.addHandler(self.shell)
        path = self.args.get('path')
        if(path and not 'unset' == path):
            if(self.args.get('newfile')):
                try:
                    from os import remove
                    remove(path)
                except OSError:
                    pass
            self.file = logging.FileHandler(path)
            self.file.setFormatter(formatter)
            self.logger.addHandler(self.file)
        return self

class ProcessStop(Exception):
    pass

class ProcessEngine(object):
    def __init__(self):
        self.events = {'kill-process':self.killer,'kill-event':self.decorate}
        self.args = {'id':'unset','oops':None,'kills':['kill-video','kill-gamepad','kill-gpio','kill-socket']}
        self.flag = True
        self.emitter = None
        self.pid = __import__('os').getpid()
        from threading import Event
        self.lock = Event()
        from signal import signal, SIGTERM, SIGINT
        signal(SIGINT,self.interrupt) # SIG_IGN|SIG_DFL or handler
        signal(SIGTERM,self.interrupt)

    def decorate(self,arguments):
        keys = arguments.keys()
        for key in keys:
            if('kills' == key):
                self.args.get('kills').append(arguments.get(key))
            else:
                self.args[key] = arguments.get(key)
        return self

    def create(self,dispatcher):
        dispatcher.attach(self.events)
        self.emitter = dispatcher
        identifier = self.args.get('id')
        if 'unset' == identifier:
            logging.error('no process id set. set process id')
            return self
        deamons = ProcessDeamon().create()
        deamon = deamons.read(identifier)
        if None == deamon:
            deamon = deamons.initialize(identifier).read(identifier)
        deamon['pid'] = self.pid
        deamons.update(identifier,deamon).write()
        return self

    def start(self,data={}):
        logging.info('process engine %s started'%(self.pid))
        try:
            from signal import pause
            # from time import sleep
            while self.flag:
                pause() # stop thread, signal handler keeps reacting
            #    self.lock.wait() # stop thread, signal handler not reacting
            #    sleep(3600) # stop thread, signal handler keeps reacting
        except self.args['oops'] as e:
            logging.error('process engine %s exception %s'%(self.pid,e.toString()))
        except ProcessStop as e:
            logging.info('process engine stop exception interrupt')
            self.killer(0,0)
        logging.info('process engine %s is stopped.'%(self.pid))
        return self

    def interrupt(self,sig_number,frame):
        self.killer()

    def killer(self,data={}):
        logging.info('application %s is to be killed'%self.pid)
        for event in self.args.get('kills'):
            logging.info('call %s'%event)
            self.emitter.emit(event,{})
        logging.info('application %s has been killed'%self.pid)
        self.kill()

    def kill(self,data={}):
        identifier = self.args.get('id')
        deamons = ProcessDeamon().create()
        deamon = deamons.read(identifier)
        if None == deamon:
            logging.error('illegal process id. hells kitchen corrupt? call kill -9 %s'%self.pid)
            return self
        deamon['pid'] = 0
        deamons.update(identifier,deamon).write()
        self.flag = False
        from signal import alarm
        # self.lock.set() # unlock thread
        from os import system
        system('kill -9 %s'%self.pid)
        return self

class ProcessDeamon(object):
    def __init__(self):
        self.path = 'hells.kitchen'
        self.parser = None
        self.deamons = {}

    def initialize(self,key):
        self.deamons[key] = {'pid':0,'host':0,'port':0}
        return self

    def create(self):
        from configparser import ConfigParser
        self.parser = ConfigParser()
        self.parser.read(self.path)
        deamons = self.parser['deamons']
        from ast import literal_eval
        for deamon in deamons:
            self.deamons[deamon] = literal_eval(deamons[deamon])
        return self

    def read(self,key):
        if key in self.deamons.keys():
            return self.deamons.get(key)
        else:
            return None

    def update(self,key,data={'pid':0,'host':0,'port':0}):
        if key in self.deamons.keys():
            vals = self.deamons[key]
            keys = vals.keys()
            for k in data:
                if k in keys:
                    vals[k] = data.get(k)
        self.write()
        return self

    def delete(self,key):
        if key in self.deamons.keys():
            del self.deamons[key]
        else:
            logging.info('not found is remvoed')
        return self

    def write(self):
        for key in self.deamons.keys():
            self.parser['deamons'][key] = str(self.deamons.get(key))
        with open(self.path, 'w') as data:
            self.parser.write(data)

class ProcessShell(object):

    def start(self,argv): # start all
        from sys import argv, stdin, stdout, stderr
        from subprocess import call, Popen
        from os import getcwd
        try:
        #    call('python %s/start.py %s'%(getcwd(),' '.join(argv[1:])), stdin=stdin, stdout=stdout, stderr=stderr, shell=True, close_fds=True) # blocking
            Popen(['python','%s/start.py'%getcwd()]+argv[1:]+['&']) # non-blocking
        except KeyboardInterrupt as e:
            pass
        exit(0)

    def kill(self): # kill all
        deamons = ProcessDeamon().create()
        deamon = deamons.read('app')
        if None == deamon:
            logging.error('illegal process id. hells kitchen corrupt?')
            return 
        from Socket import SocketClient
        SocketClient().send({'call':'kill-process'},host=deamon.get('host'),port=deamon.get('port'))

    def state(self):
        logging.error('kill not implemented')
        # open socket client
        # check state

    def video(self):
        logging.error('kill not implemented')
        # open socket client
        # send event...

class ProcessArguments(object):
    def __init__(self):
        self.holder = {}
    #    self.events = {}
        self.logOpt = {}

    def decorate(self,arguments): # register new cmd line args
        for key in arguments:
            if not key in self.holder:
                self.holder[key] = arguments[key]
        return self

    def create(self,dispatcher):
        from sys import exit, argv
        from getopt import getopt, GetoptError
        try:
            opts, args = getopt(argv[1:],shortopts=''.join(self.holder.values()),longopts=self.holder.keys())
            for o, a in opts: # must be at the beginning of input
                if '--verbose' == o:self.logOpt['level'] = a
                elif '--logfile' == o:self.logOpt['path'] = a
                elif '--noshell' == o:self.logOpt['shell'] = False

                elif '--test' == o:print 'test test test'
                # elif '--driver' == o:appOpts['driver'] = a
            return self
        except GetoptError as e:
            from logging import error
            error(e.msg)
            exit(2)

    def logger(self):
        return self.logOpt

    def deliver(self):
        # send options via events to moduls
        return self

