#!/usr/bin/python
import logging

class VideoListener(object):
    def __init__(self):
        self.events = {'initialize-video':self.initialize}
        self.emitter = None

    def decorate(self,arguments):
        if 'emitter' in arguments.keys():
            self.emitter = arguments.get('emitter')
            self.emitter.attach(self.events)            

    def initialize(self,data):
        logging.info('receive initialize-video from %s'%(data.get('host')))
        data = {'call':'video-initialized','id':'initialize-video','namespace':'video'}
        from Process import ProcessDeamon
        deamons = ProcessDeamon().create().deamons
        for key in deamons.keys():
            if 'cam' in key:
                camera = deamons.get(key)
                if not '0' == camera.get('host') and not 0 == camera.get('port'):
                    data[key] = {'url':'http://%s:%s/?action=stream'%(camera.get('host'),camera.get('port'))}
        self.emitter.emit('push-sio',data)

if __name__ == "__main__":
    from sys import exit, path
    path.append('share')
    
    from Network import SocketServer, EventNetwork
    application = EventNetwork().decorate({'trace':True})
    SocketServer().decorate({'emitter':application,'id':'web','port':9002,'deamon':True})
    VideoListener().decorate({'emitter':application})
    #########################
    ###   load from cfg   ###
    #########################
    firebase = {
        'emitter':application
    }
    #########################
    ###   load from cfg   ###
    #########################
    from Firebase import Firebase
    Firebase().decorate(firebase)

    from Process import ProcessLogger, ProcessEngine
    logger = ProcessLogger().decorate({'emitter':application})
    engine = ProcessEngine().decorate({'emitter':application,'id':'web','services':['create-socket','create-cgi','create-firebase']})

    from Cgi import Cgi, CgiSocket
    cgi = Cgi().decorate({'emitter':application,'logger':logger.logger})
    CgiSocket().decorate({'emitter':application,'namespace':'video'}).create(cgi.socket)
    CgiSocket().decorate({'emitter':application,'namespace':'drive'}).create(cgi.socket)

    from Options import Options
    Options().decorate({'emitter':application}).create().deliver()
    engine.create()
    exit(0)