import logging, json, struct

class SocketClient(object):
    def __init__(self):
        # blocking mode: timeout=None
        self.args = {'host':'localhost','port':'unset','framesize':4096,'timeout':5,'payload':'large','deamon':False}

    def decorate(self,arguments):
        keys = self.args.keys()
        for key in arguments:
            if key in keys:
                self.args[key] = arguments[key]
        return self

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
                    ,'reply':False,'payload':'large','deamon':False}
        self.server = None
        self.thread = None
        self.reply = {'call':'net-event','data':'no reply server response from %s:%s'%(self.args.get('host'),self.args.get('port'))}
        self.emitter = None
        self.listening = False

    def decorate(self,arguments):
        keys = self.args.keys()
        for key in arguments:
            if key in keys:
                self.args[key] = arguments[key]
        return self

    def create(self,dispatcher):
        dispatcher.attach(self.events) # register own events
        self.emitter = dispatcher
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
            from Util import ProcessDeamon
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
            logging.info('socket created on %s:%s'%(host,port))
            from threading import Thread
            self.thread = Thread(target=self.listen)
            # self.thread = threading.Thread(target=self.listen,args=[server,receive,sender])
            self.thread.setDaemon(self.args.get('deamon'))
            self.thread.start()
            self.reply = {'call':'net-event','data':'no reply server response from %s:%s'%(host,port)}
        except timeout, msg:
            logging.error('server timeout error! server kill forced! %s:%s %s'%(host,port,msg))
        except gaierror, msg: # socket get address/name info errors
            logging.error('server get address info error! server kill forced! %s:%s %s'%(host,port,msg))
        except herror, msg:  # socket address related errors
            logging.error('server host error! server kill forced! %s:%s %s'%(host,port,msg))
        except error, msg:
            logging.error('server default error! server kill forced! %s:%s %s'%(host,port,msg))
        return self

    def listen(self):
        logging.info('socket listening on %s:%s'%(self.args.get('host'),self.args.get('port')))
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
        from Util import ProcessDeamon
        deamons = ProcessDeamon().create()
        deamon = deamons.read(identifier)
        if None == deamon:
            logging.error('illegal process id. hells kitchen corrupt?')
            return self
        deamon['host'] = "0"
        deamon['port'] = 0
        deamons.update(identifier,deamon).write()
        logging.info('socket on %s:%s stopped'%(self.args.get('host'),self.args.get('port')))
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

def reader(c,n): # recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = c.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
