
if __name__ == "__main__":
    
    from Util import ProcessArguments, ProcessDispatcher, ProcessLogger, ProcessEngine, ProcessDeamon
    application = ProcessDispatcher().decorate({'trace':True})

    args = ProcessArguments().decorate({'verbose=':'','logfile=':'','noshell':''}) \
                           .decorate({'test':'t'}) \
                           .create(application)

    ProcessLogger().decorate(args.logger()).create(application)
    # application.emit('logger-options',args.logger())
    engine = ProcessEngine().decorate({'id':'app'}).create(application) #.decorate(appOpts)

    
    from Socket import SocketServer
    SocketServer().decorate({'id':'app','port':9001,'deamon':True}).create(application)

    from Driver import GamepadDriver
    GamepadDriver().create(application)

    from Video import Cameras, VideoStream
    Cameras().create(application)

    from Gpio import Gpios
    Gpios().create(application).start()

    application.emit('start-video',{})
    application.emit('start-gamepad',{})

    engine.start()

    from sys import exit
    exit(0)