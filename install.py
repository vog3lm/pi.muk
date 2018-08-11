
def apt(packages):
    process = Popen(['apt-get','-y','install']+packages)
    process.communicate()

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
    from pip.__main__ import _main as install
    # share
    install(['install','--upgrade','configparser'])
    # app
    install(['install','--upgrade','inputs'])
    install(['install','--upgrade','pynput'])
    # web
    install(['install','--upgrade','flask'])
    install(['install','--upgrade','flask-socketio'])
    install(['install','--upgrade','flask-login'])
    install(['install','--upgrade','flask-sse'])

    #install(['install','--upgrade','Pyrebase']) #?
    #install(['install','--upgrade','yowsup2']) # whats app

    from subprocess import Popen
    process = Popen(['apt-get','update'])
    process.communicate()
    # mjpg streamer
    apt(['build-essential','libjpeg8-dev','imagemagick','libv4l-dev','cmake'])
    #process = Popen(['cd','/tmp','git','clone','https://github.com/vog3lm/mjpg-streamer.git','make','sudo','make','install'])
    #process.communicate()
    # tools
    #apt(['nmap','wireshark','john','hydra','aircrack-ng'])
    #Popen(['wget','https://downloads.metasploit.com/data/releases/metasploit-latest-linux-x64-installer.run'
    #      ,'wget','https://downloads.metasploit.com/data/releases/metasploit-latest-linux-x64-installer.run.sha1'
    #      ,'echo','$(cat metasploit-latest-linux-x64-installer.run.sha1)'
    #             ,'metasploit-latest-linux-x64-installer.run > metasploit-latest-linux-x64-installer.run.sha1 '
    #      ,'shasum','-c','metasploit-latest-linux-x64-installer.run.sha1'
    #      ,'chmod','+x','./metasploit-latest-linux-x64-installer.run','&&','./metasploit-latest-linux-x64-installer.run'])
    #process.communicate()

    # OWASP Zed
    # Reaver
    # oclHashcat # handshake gpu capture
    # Crunch # wordlist attack
    # Macchanger

    #Popen(['ssl/.ssl.sh','--install','--create'])
    #p.communicate

    from logging import info, error
    from os import getcwd, system, path
    from share.Process import ProcessLogger, ProcessDeamon
    ProcessLogger().decorate({}).create()
    fn = '%s/hells.kitchen'%getcwd()
    create(fn,['[deamons]'])
    check(fn,'deamon configuration file')
    ProcessDeamon().create().initialize('app').initialize('web').write()
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
        ,"elif 'restart' == command:\n"
        ,"    ProcessShell().restart(service)\n"
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






