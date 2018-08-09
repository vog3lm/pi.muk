
def install(apt,pn):
    pkg = apt[pn]
    if not pkg.is_installed:
        pkg.mark_install()
        try:
            apt.commit()
        except Exception as e:
            error('install %s error, %s'%(pn,str(e)))

def check(fn,msg):
    if path.exists(fn):
        info('%s installed (%s)'%(msg,fn))
    else:
        error('%s not installed'%(msg))

def create(fn,lines):
    try:
        with open(fn,'w+') as f:
            if(not f == None):
                f.writelines(lines)
            system("sudo chmod 777 %s"%fn)
    except IOError as e:
        error("install %s error, %s"%(fn,e.strerror))


if __name__ == "__main__":
    from logging import info, error

    # install mjpeg-streamer
    # Update & Install Tools
    #sudo apt-get -y update

    from apt.cache import Cache
    #apt = Cache()
    #apt.update()
    #apt.open()
    #install(apt,'build-essential') #sudo apt-get -y install build-essential libjpeg8-dev imagemagick libv4l-dev cmake
    #install(apt,'libjpeg8-dev')
    #install(apt,'imagemagick')
    #install(apt,'libv4l-dev')
    #install(apt,'cmake')
    #Popen(['cd','/tmp'])
    #Popen(['git','clone','https://github.com/jacksonliam/mjpg-streamer.git']) # git clone https://github.com/jacksonliam/mjpg-streamer.git
    #Popen(['cd','mjpg-streamer/mjpg-streamer-experimental'])
    #Popen(['make'])
    #Popen(['sudo','make','install'])

    from pip import main
    #main(['install', 'configparser'])
    #main(['install', 'inputs'])
    #main(['install', 'pynputs'])

    #main(['install', 'flask'])
    #main(['install', 'flask-socketio'])
    #main(['install', 'flask-login'])
    #main(['install', 'flask-sse'])

    #main(['install', 'Pyrebase']) #?

    from os import getcwd, system, path
    from Util import ProcessLogger
    ProcessLogger().decorate({}).create()

    fn = '%s/hells.kitchen'%getcwd()
    create(fn,['[deamons]'])
    check(fn,'deamon configuration file')

    fn = '/bin/muk'
    lines = ["#!/usr/bin/python\n"
        ,"from os import chdir\n"
        ,"chdir('%s')\n"%(getcwd())
        ,"from sys import path, argv, exit\n"
        ,"path.append('%s')\n"%(getcwd())
        ,"from Util import ProcessLogger, ProcessShell\n"
        ,"command = argv[1]\n"
        ,"if 'start' == command:\n"
        ,"    ProcessShell().start(argv[2:])\n"
        ,"elif 'kill' == command:\n"
        ,"    ProcessShell().kill()\n"
        ,"else:\n"
        ,"    from logging import error\n"
        ,"    error('unknown muk command %s. [start|kill]'%command)\n"
        ,"exit(0)\n"
    ]
    create(fn,lines)
    check(fn,'shell environment variable')






