if __name__ == "__main__":
    from sys import exit, path
    path.append('share')
    from Network import SocketServer, EventNetwork
    application = EventNetwork().decorate({'trace':True})


#    from Driver import GamepadDriver
#    GamepadDriver().decorate({'emitter':application})
#    from Video import Cameras, VideoStream
#    Cameras().decorate({'emitter':application})
#    from Gpio import Gpios
#    Gpios().decorate({'emitter':application}) # .create().start()


    from Process import ProcessLogger, ProcessEngine, ProcessArguments
    logger = ProcessLogger().decorate({'emitter':application})
    server = SocketServer().decorate({'emitter':application,'id':'app','port':9001,'deamon':True})
    engine = ProcessEngine().decorate({'emitter':application,'id':'app'})
    ###
    ProcessArguments().decorate({'emitter':application,'verbose=':'','logfile=':'','noshell':''}).create() # .deliver()
    ###
    logger.create() # call as service from engine

    # application.emit('start-video',{})
    # application.emit('start-gamepad',{})

    server.create()
    engine.create()
    exit(0)