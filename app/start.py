#!/usr/bin/python
if __name__ == "__main__":
    from sys import exit, path
    path.append('share')

    from Network import SocketServer, EventNetwork
    application = EventNetwork().decorate({'trace':True})
    server = SocketServer().decorate({'emitter':application,'id':'app','port':9001,'deamon':True})

    from Driver import GamepadDriver, RemoteDriver
#    GamepadDriver().decorate({'emitter':application})
    RemoteDriver().decorate({'emitter':application})

    from Video import Cameras
    Cameras().decorate({'emitter':application})

    from Gpio import Gpios
    Gpios().decorate({'emitter':application}) # .create().start()

    from Firebase import FirebaseServer
    server = FirebaseServer().decorate({'emitter':application}).configurate() #.create()

    from Process import ProcessLogger, ProcessEngine
    logger = ProcessLogger().decorate({'emitter':application})
    engine = ProcessEngine().decorate({'emitter':application,'id':'app','services':['create-socket','create-gpio','create-cameras','create-firebase-server','create-remote-driver'] 
                                                                       ,'kills':['kill-gpio','kill-socket','kill-cameras']}) # 'kill-cameras' (done by process shell)

    from Options import Options
    Options().decorate({'emitter':application}).create().deliver()

    engine.create()
    exit(0)