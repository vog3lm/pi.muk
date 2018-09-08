#!/usr/bin/python
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
    from logging import info, error
    from share.Process import ProcessLogger, ProcessDeamon
    ProcessLogger().create()
    try:
        from sys import exit, argv
        # parse options
        options = ['pip','mjpg','ssl','cli','cfg','report']
        report = False
        from getopt import getopt, GetoptError
        try:
            opts, args = getopt(argv[1:],shortopts='',longopts=options)
            options = []
        except GetoptError as e:
            error(e.msg)
            exit(1)
        for o, a in opts:
            if '--pip' == o:options.append('pip')
            elif '--mjpg' == o:options.append('mjpg')
            elif '--ssl' == o:options.append('ssl')
            elif '--cli' == o:options.append('cli')
            elif '--cfg' == o:options.append('cfg')
            elif '--report' == o:report = True
        if 0 == len(options):
            options = ['pip','mjpg','ssl','cli','cfg']
        # save root directory
        from os import getcwd, system, path
        root = getcwd()

        if 'pip' in options: # install pip dependencies
            import pip
            install = None
            if hasattr(pip,'main'):
                install = pip.main
            elif hasattr(pip,'_internal'):
                install = pip._internal.main
            if None == install:
                error("python-pip not found. call 'apt-get install python-pip'")
            else:
                packages = ['configparser','netifaces','lockfile','python-git','inputs','pynput'
                           ,'flask','flask-socketio','flask-login','flask-sse'
                        #   ,'Pyrebase','yowsup2'
                           ]
                for package in packages:
                    install(['install','--upgrade',package])
                info('%s successfully installed'%', '.join(packages))

        if 'mjpg' in options or 'other' in options:
            from subprocess import Popen
            process = Popen(['apt-get','update'])
            process.communicate()

        if 'mjpg' in options:
            # load picamera 'usb' driver
            process = Popen(['sudo','modprobe','bcm2835-v4l2']) # ,stdout=PIPE, stdin=PIPE, stderr=PIPE
            process.communicate()
            # or append bcm2835-v4l2 to /etc/modules
            # width open('/etc/modules',w+) as fn:
            #     lines = fn.readlines()
            #     if not 'bcm2835-v4l2' in lines:
            #         lines.append('bcm2835-v4l2')
            #         fn.writelines(lines)
            # mjpg streamer
            apt(['build-essential','libjpeg8-dev','imagemagick','libv4l-dev','cmake'])
            from os import chdir, listdir
            if not 'mjpg-streamer' in listdir('/tmp'):
                from git import Git
                Git('/tmp').clone('https://github.com/vog3lm/mjpg-streamer.git')
            chdir('/tmp/mjpg-streamer/mjpg-streamer-experimental/')
            process = Popen(['make'])
            process.communicate()
            process = Popen(['sudo','make','install'])
            process.communicate()
            chdir(root)
            info('mjpeg-streamer successfully installed')


        if 'ssl' in options: # install ssl key/crt
            process = Popen(['ssl/./ssl.sh','--install','--create'])
            process.communicate()
            info('ssl keys and certificates successfully installed')

        if 'cli' in options:
            fn = '/bin/muk'
            lines = ["#!/usr/bin/python\n"
                ,"from os import chdir\n"
                ,"chdir('%s')\n"%root
                ,"from sys import path, argv, exit\n"
                ,"path.append('%s')\n"%root
                ,"from share.Process import ProcessShell\n"
                ,"ProcessShell(argv)\n"
                ,"exit(0)"]
            create(fn,lines)
            check(fn,'shell environment variable')

        if 'cfg' in options:
            fn = '%s/hells.kitchen'%root
            create(fn,['[deamons]'])
            check(fn,'deamon configuration file')
            ProcessDeamon().create().initialize('app').initialize('web').write()

        if report:
            length = 0
            lines = []
            for option in options:
            	lines.append('%s successfully installed'%option)
            for line in lines:
                if length < len(line):
                    length = len(line)
            div = '-'*(length+4)
            print '%s\n  %s\n%s'%(div,'\n  '.join(lines),div)

        exit(0)
    except KeyboardInterrupt as e:
        info('installation canceled')
        exit(2)

