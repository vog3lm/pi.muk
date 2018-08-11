import logging, json, struct

def reader(c,n): # recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = c.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

class EventNetwork(object):
    def __init__(self):
        self.events = {}
        self.args = {'trace':False}
        self.flag = True
        from queue import Queue
        self.queue = Queue()
        from threading import Thread, Event
        self.lock = Event()
        self.thread = Thread(target=self.thread,args=[self.queue])
        self.thread.setDaemon(True)
        self.thread.start()

    def decorate(self,arguments):
        from Process import decorate
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

    def threaded(self,call,data):
        data['call'] = call
        self.queue.put(data)
        self.lock.set()

    def thread(self,queue):
        while self.flag:
            self.lock.wait()
            data = queue.get()
            self.emit(data.get('call'),data)
            queue.task_done()

class SocketClient(object):
    def __init__(self):
        # blocking mode: timeout=None
        self.args = {'host':'localhost','port':'unset','framesize':4096,'timeout':5,'payload':'large','deamon':False}

    def decorate(self,arguments):
        from Process import decorate
        return decorate(self,arguments)

    def send(self,data,host=None,port=None):
        if(None == host):
            host = self.args.get('host')
        if(None == port):
            port = self.args.get('port')
        from socket import socket, timeout, gaierror, herror, error
        from json import dumps
        try:
            client = socket()
            client.settimeout(self.args.get('timeout'))
            client.connect((host,int(port))) # errors: connection refused
            logging.debug('socket send %s to %s:%s'%(data,host,port))
            response = self.large(client,dumps(data))
            client.close()
            return response
        except timeout, msg:
            logging.error('client timeout error! client kill forced! %s:%s %s'%(host,port,msg))
        except gaierror, msg: # socket get address/name info errors
            logging.error('client get address info error! client kill forced! %s:%s %s'%(host,port,msg))
        except herror, msg:  # socket address related errors
            logging.error('client host error! client kill forced! %s:%s %s'%(host,port,msg))
        except error, msg:
            logging.error('client default error! client kill forced! %s:%s %s'%(host,port,msg))

    def small(self,c,data): # small payload
        c.send(data)
        return c.recv(self.args.get('framesize'))

    def large(self,c,data): # large payload
        data = struct.pack('>I', len(data)) + data
        c.sendall(data)
        # Read message length and unpack it into an integer
        raw_msglen = reader(c, 4)
        if raw_msglen:
            msglen = struct.unpack('>I', raw_msglen)[0]
            # Read the message data
            return reader(c, msglen)
        return {'data':'no server response'}

class SocketServer(object):
    def __init__(self):
        self.events = {'kill-socket':self.kill}
        from socket import SOCK_STREAM, AF_INET
        self.args = {'id':'unset','host':'127.0.0.1','port':'unset','clients':5,'transport':SOCK_STREAM,'protocol':AF_INET,'framesize':4096,'timeout':None
                    ,'reply':False,'payload':'large','deamon':False,'emitter':None}
        self.server = None
        self.thread = None
        self.reply = {'call':'net-event','data':'no reply server response from %s:%s'%(self.args.get('host'),self.args.get('port'))}
        self.emitter = None
        self.listening = False

    def decorate(self,arguments):
        from Process import decorate
        return decorate(self,arguments)

    def create(self):
        self.emitter = self.args.get('emitter')
        host = self.args.get('host')
        port = self.args.get('port')
        try:
            from socket import socket, timeout, gaierror, herror, error, SOL_SOCKET, SO_REUSEADDR
            import threading, struct
            self.server = socket(self.args.get('protocol'),self.args.get('transport')) 
            self.server.settimeout(self.args.get('timeout')) 
            self.server.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
            self.server.bind((host,port))
            # self.server.setblocking(True) # def:True = 0, 
            self.server.listen(self.args.get('clients'))
            self.args['host'], self.args['port'] = self.server.getsockname()
            from Process import ProcessDeamon
            identifier = self.args.get('id')
            deamons = ProcessDeamon().create()
            deamon = deamons.read(identifier)
            if None == deamon:
                logging.error('illegal process id.')
                return self
            deamon['host'] = host
            deamon['port'] = port
            deamons.update(identifier,deamon)
            deamons.write()
            logging.info('%s socket created on %s:%s'%(self.args.get('id'),host,port))
            from threading import Thread
            self.thread = Thread(target=self.listen)
            # self.thread = threading.Thread(target=self.listen,args=[server,receive,sender])
            self.thread.setDaemon(self.args.get('deamon'))
            self.thread.start()
            self.reply = {'call':'net-event','data':'no reply server response from %s:%s'%(host,port)}
        except timeout, msg:
            logging.error('%s server timeout error! server kill forced! %s:%s %s'%(self.args.get('id'),host,port,msg))
        except gaierror, msg: # socket get address/name info errors
            logging.error('%s server get address info error! server kill forced! %s:%s %s'%(self.args.get('id'),host,port,msg))
        except herror, msg:  # socket address related errors
            logging.error('%s server host error! server kill forced! %s:%s %s'%(self.args.get('id'),host,port,msg))
        except error, msg:
            logging.error('%s server error! server kill forced! %s:%s %s'%(self.args.get('id'),host,port,msg))
        return self

    def listen(self):
        logging.info('%s socket listening on %s:%s'%(self.args.get('id'),self.args.get('host'),self.args.get('port')))
        self.listening = True
        from ast import literal_eval
        while self.listening:
            connection, client = self.server.accept()
            logging.info("socket event on %s:%s"%(self.args.get('host'),self.args.get('port')))
            string = self.large(connection)
            nto = literal_eval(string)
            logging.debug("received event data: %s"%nto)
            self.emitter.emit(nto.get('call'),nto)

    def kill(self,data={}):
        self.listening = False
        self.server.close()
        identifier = self.args.get('id')
        from Process import ProcessDeamon
        deamons = ProcessDeamon().create()
        deamon = deamons.read(identifier)
        if None == deamon:
            logging.error('illegal process id. hells kitchen corrupt?')
            return self
        deamon['host'] = "0"
        deamon['port'] = 0
        deamons.update(identifier,deamon).write()
        logging.info('%s socket on %s:%s stopped'%(self.args.get('id'),self.args.get('host'),self.args.get('port')))
        return self

    def small(self,c): # small payload
        string = connection.recv(self.args.get('framesize'))
        if(not self.args.get('reply')):
            c.send(json.dumps(self.reply))
        return string

    def large(self,c): # large payload
        string =  None
        # Read message length and unpack it into an integer
        raw_msglen = reader(c, 4)
        if raw_msglen:
            msglen = struct.unpack('>I', raw_msglen)[0]
            # Read the message data
            string = reader(c, msglen)
        if(not self.args.get('reply')):
            reply = json.dumps(self.reply)
            c.sendall(struct.pack('>I', len(reply)) + reply)
        return string

    def response(self,c,dto):
        responose = json.dumps(dto)
        c.sendall(struct.pack('>I', len(responose)) + responose)
