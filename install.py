
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

    #from pip import main
    #main(['install', 'getopts'])
    #main(['install', 'configparser'])
    #main(['install', 'inputs'])
    #main(['install', 'pynputs'])

    #main(['install', 'flask'])
    #main(['install', 'flask-socketio'])
    #main(['install', 'flask-login'])
    #main(['install', 'flask-sse'])

    #main(['install', 'Pyrebase']) #?
    #main(['install', 'yowsup2']) # whats app


    # install mjpeg-streamer
    # Update & Install Tools
    #sudo apt-get -y update

    #from apt.cache import Cache
    #apt = Cache()
    #apt.update()
    #apt.open()

    #install(apt,'build-essential') #sudo apt-get -y install build-essential libjpeg8-dev imagemagick libv4l-dev cmake
    #install(apt,'libjpeg8-dev')
    #install(apt,'imagemagick')
    #install(apt,'libv4l-dev')
    #install(apt,'cmake')
    #Popen(['cd','/tmp'])
    #Popen(['git','clone','https://github.com/vog3lm/mjpg-streamer.git']) # git clone https://github.com/vog3lm/mjpg-streamer.git
    #Popen(['cd','mjpg-streamer/mjpg-streamer-experimental'])
    #Popen(['make'])
    #Popen(['sudo','make','install'])


    # apt-get -y install nmap
    # apt-get -y install wireshark
    # apt-get -y install john # john the ripper
    # apt-get -y install hydra
    # apt-get -y install aircrack-ng

    # wget https://downloads.metasploit.com/data/releases/metasploit-latest-linux-x64-installer.run
    # wget https://downloads.metasploit.com/data/releases/metasploit-latest-linux-x64-installer.run.sha1
    # echo $(cat metasploit-latest-linux-x64-installer.run.sha1)'  'metasploit-latest-linux-x64-installer.run > metasploit-latest-linux-x64-installer.run.sha1 
    # shasum -c metasploit-latest-linux-x64-installer.run.sha1
    # chmod +x ./metasploit-latest-linux-x64-installer.run && sudo ./metasploit-latest-linux-x64-installer.run

    # OWASP Zed
    # Reaver
    # oclHashcat # handshake gpu capture
    # Crunch # wordlist attack
    # Macchanger



    from os import getcwd, system, path
    from share.Process import ProcessLogger
    ProcessLogger().decorate({}).create()
    fn = '%s/hells.kitchen'%getcwd()
    create(fn,['[deamons]'])
    check(fn,'deamon configuration file')
    fn = '/bin/muk'
    lines = ["#!/usr/bin/python\n"
        ,"from os import chdir\n"
        ,"chdir('%s')\n"%getcwd()
        ,"from sys import path, argv, exit\n"
        ,"path.append('%s')\n"%getcwd()
        ,"command = argv[1]\n"
        ,"service = 'all'\n"
        ,"for i in argv[1:]:\n"
        ,"    if '--only' in i:\n"
        ,"        service = i[7:]\n"
        ,"        argv.remove(i)\n"
        ,"        break\n"
        ,"from share.Process import ProcessShell\n"
        ,"if 'start' == command:\n"
        ,"    ProcessShell().start(service,argv[2:])\n"
        ,"elif 'reset' == command:\n"
        ,"    ProcessShell().reset(service)\n"
        ,"elif 'kill' == command:\n"
        ,"    ProcessShell().kill(service)\n"
        ,"elif 'reset' == command:\n"
        ,"    ProcessShell().reset(service)\n"
        ,"elif 'state' == command:\n"
        ,"    ProcessShell().state(service)\n"
        ,"elif 'help' == command:\n"
        ,"    ProcessShell().help(service)\n"
        ,"else:\n"
        ,"    print \"%s is unknown. call 'muk help' for MORE information.\"%command\n"
        ,"exit(0)"]
    create(fn,lines)
    check(fn,'shell environment variable')






