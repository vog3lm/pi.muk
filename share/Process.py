import logging

def decorate(clazz,arguments):
    if 'emitter' in arguments.keys() and hasattr(clazz,'events'):
        arguments.get('emitter').attach(clazz.events)
    keys = clazz.args.keys()
    for key in arguments:
        if key in keys:
            clazz.args[key] = arguments.get(key)
    return clazz

class ProcessLogger(object):
    def __init__(self):
        # log levels
            # CRITICAL  50
            # ERROR     40
            # WARNING   30
            # INFO      20
            # DEBUG     10
            # NOTSET     0
        self.events = {'create-logger':self.create,'logger-options':self.decorate}
        self.args = {'path':'unset','level':20,'newfile':True,'shell':True
                    ,'format':'%(asctime)18s %(levelname)7s >> %(process)6s %(module)s.%(funcName)s():%(lineno)d >> %(message)s'
                    ,'date':'%Y-%m-%d %H:%M:%S'}
        self.logger = logging.getLogger()
        self.file = None
        self.shell = None

    def decorate(self,arguments):
        return decorate(self,arguments)

    def create(self,data={}):
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
        self.events = {'kill-process':self.kill,'kill-event':self.decorate,'service-event':self.decorate}
        self.args = {'id':'unset','oops':None,'kills':['kill-video','kill-gamepad','kill-gpio','kill-socket'],'services':[]}
        self.flag = True
        self.emitter = None
        # from threading import Event
        # self.lock = Event()
        from signal import signal, SIGTERM, SIGINT
        signal(SIGINT,self.killer) # SIG_IGN|SIG_DFL or handler
        signal(SIGTERM,self.killer)
        from os import getpid
        self.pid = getpid()

    def decorate(self,arguments):
        if 'emitter' in arguments.keys():
            arguments.get('emitter').attach(self.events)
        keys = arguments.keys()
        for key in keys:
            if('kills' == key):
                self.args.get('kills').append(arguments.get(key))
            elif('services' == key):
                self.args.get('services').append(arguments.get(key))
            else:
                self.args[key] = arguments.get(key)
        return self

    def create(self,data={}):
        self.emitter = self.args.get('emitter')
        if None == self.emitter:
            logging.error('no event dispatcher set')
            return self
        identifier = self.args.get('id')
        if 'unset' == identifier:
            logging.error('no process id set. set process id')
            return self

        for service in self.args.get('services'):
            self.emitter.emit(service,{'call':service,'id':'create-process'})

        deamons = ProcessDeamon().create()
        deamon = deamons.read(identifier)
        if None == deamon:
            deamon = deamons.initialize(identifier).read(identifier)
        deamon['pid'] = self.pid
        deamons.update(identifier,deamon).write()

        logging.info('%s process engine %s started'%(self.args.get('id'),self.pid))
        try:
            from signal import pause
            # from time import sleep
            while self.flag:
                pause() # stop thread, signal handler keeps reacting
            #    self.lock.wait() # stop thread, signal handler not reacting
            #    sleep(3600) # stop thread, signal handler keeps reacting
        except self.args['oops'] as e:
            logging.error('%s process engine %s error exception. %s'%(self.args.get('id'),self.pid,e.toString()))
        except ProcessStop as e:
            logging.info('%s process engine %s stop exception'%(self.args.get('id'),self.pid))
            self.kill()
        logging.info('%s process engine %s is stopped.'%(self.args.get('id'),self.pid))
        return self

    def killer(self,sig,frame):
        self.killer()

    def kill(self,data={}):
        logging.info('%s (%s) is to be killed'%(self.args.get('id'),self.pid))
        for event in self.args.get('kills'):
            logging.info('call %s'%event)
            self.emitter.emit(event,{})
        logging.info('%s (%s) has been killed'%(self.args.get('id'),self.pid))
        identifier = self.args.get('id')
        deamons = ProcessDeamon().create()
        deamon = deamons.read(identifier)
        if None == deamon:
            id = self.args.get('id')
            logging.error("illegal %s process id. hells kitchen corrupt? call 'muk reset --only=%s'"%(id,id))
            return self
        deamon['pid'] = 0
        deamons.update(identifier,deamon).write()
        self.flag = False
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
        self.deamons[key] = {'pid':0,'host':'0','port':0}
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
        self.create()
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

class ProcessShell(object): # directly called from /bin/muk
    def __init__(self):
        self.services = ['app','web']
        self.deamons = ProcessDeamon().create()

    def start(self,service,argv):
        if service in self.services:
            self.services = [service]
        from time import sleep
        for service in self.services:
            deamon = self.deamons.read(service)
            if None == deamon or not 'pid' in deamon.keys():
                logging.error('illegal process id. hells kitchen corrupt?')
            elif not 0 == deamon.get('pid'):
                print "%s is running on pid %s. call 'muk restart %s' or muk kill %s"%(service,deamon.get('pid'),service,service)
            else:
                from subprocess import Popen
                prc = Popen(['python','%s/start.py'%service]+argv) # non-blocking
                sleep(0.1)

    def restart(self,service,argv):
        if service in self.services:
            self.services = [service]
        for service in self.services:
            deamon = self.deamons.read(service)
            logging.error('restart %s with new options not implemented'%service)

    def kill(self,service):
        if service in self.services:
            self.services = [service]
        from share.Network import SocketClient
        client = SocketClient()
        from time import sleep
        for service in self.services:
            deamon = self.deamons.read(service)
            if None == deamon or not 'port' in deamon.keys():
                logging.error('illegal process id. hells kitchen corrupt?')
            elif 0 == deamon.get('port'):
                print "%s is offline"%service
            else:
                client.send({'call':'kill-process'},host=deamon.get('host'),port=deamon.get('port'))
                sleep(0.1)

    def reset(self,service):
        if service in self.services:
            self.services = [service]
        from subprocess import Popen, PIPE
        for service in self.services:
            process = Popen(["pidof","python %s/start.py *"%service],stdout=PIPE,stdin=PIPE,stderr=PIPE)
            pid, err = process.communicate()
            logging.warning('not working correctly, out=%s err=%s'%(pid,err))
            if not '' == pid:
                Popen(['kill','-9 %s'%pid])
            self.deamons.initialize(service).write()

    def state(self,service):
        if service in self.services:
            self.services = [service]
        for service in self.services:
            deamon = self.deamons.read(service)
            logging.error('reset %s not implemented'%service)
            # open socket client
            # check state

    def help(self,service):
        lines = ['\n Usage: muk [command] [options]']
        if service in self.services:
            self.services = [service]
        else:
            lines = lines + ['\n Commands:\n'
                            ,' help......................: '
                            ,' kill [arguments]..........: '
                            ,' restart [arguments].......: '
                            ,' start [arguments].........: '
                            ,' state [arguments].........: '
                            ,'\n Shell Options:\n'
                            ,' [    | --only ]...........: ']
        print '\n '.join(lines)
        from pydoc import locate
        for service in self.services:
            print '\n '.join(locate('%s.Properties.help'%service))

class ProcessArguments(object):
    def __init__(self):
        self.args = {'emitter':None}
    #    self.events = {}
        self.logOpt = {}

    def decorate(self,arguments): # register new cmd line args
        return decorate(self,arguments)

    def create(self):
        self.emitter = self.args.get('emitter')

        del self.args['emitter']
        from sys import exit, argv
        from getopt import getopt, GetoptError
        try:
            opts, args = getopt(argv[1:],shortopts=''.join(self.args.values()),longopts=self.args.keys())
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
        self.emitter.emit('logger-options',self.logOpt)
        return self