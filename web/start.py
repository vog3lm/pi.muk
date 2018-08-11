#!/usr/bin/python
if __name__ == "__main__":
    from sys import exit, path
    path.append('share')
    from Network import SocketServer, EventNetwork
    application = EventNetwork().decorate({'trace':True})
    

    from Process import ProcessLogger, ProcessEngine, ProcessArguments
    logger = ProcessLogger().decorate({'emitter':application})
    server = SocketServer().decorate({'emitter':application,'id':'web','port':9002,'deamon':True})
    engine = ProcessEngine().decorate({'emitter':application,'id':'web'})
    ###
    ProcessArguments().decorate({'emitter':application,'verbose=':'','logfile=':'','noshell':''}).create().deliver()
    ###
    logger.create() # call as service from engine

    # application.emit('start-video',{})
    # application.emit('start-gamepad',{})
    
    server.create()
    engine.create()
    exit(0)