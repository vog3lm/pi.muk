import logging

#               >  mjpg_streamer -i "/usr/local/lib/mjpg-streamer/input_uvc.so -d /dev/video0 -r 640x480 -f 15' -n -y" -o "/usr/local/lib/mjpg-streamer/output_http.so -n /usr/local/www -p 8080"
#               >  mjpg_streamer -i "/usr/local/lib/mjpg-streamer/input_uvc.so -d /dev/video0 -r 512x288 -f 15' -n" -o "/usr/local/lib/mjpg-streamer/output_http.so -n -p 8080"
#               >  mjpg_streamer -i "/usr/local/lib/mjpg-streamer/input_uvc.so -d /dev/video0 -r 512x288 -f 10' -n -u -q 50" -o "/usr/local/lib/mjpg-streamer/output_http.so -n -p 8080"
# very nice !!  >  mjpg_streamer -i "/usr/local/lib/mjpg-streamer/input_uvc.so -d /dev/video0 -r 768x432 -f 10' -n -u -q 50" -o "/usr/local/lib/mjpg-streamer/output_http.so -n -p 8080"

class MjpegException(Exception):
    def __init__(self,errors):
        self.errors = errors
    def toString(self):
        return ''.join(self.errors) # str(self.errors).replace('\'','').replace('[','').replace(']','')

class MjpegStreamerUtil(object):
    def __init__(self):
        self.name = 'unset'
        self.args = {}
    def decorate(self,arguments):
        keys = self.args.keys()
        for key in arguments:
            if key in keys and not arguments[key] == 'unset':
                self.args[key] = arguments[key]
        return self
    def validate(self):
        errors = []
        keys = self.args.keys()
        for key in keys:
            if('unset' == self.args.get(key)):
                errors.append('%s value error. %s=%s'%(key,key,self.args.get(key)))
        if(0 < len(errors)):
            errors.insert(0,'%s input plugin error'%self.name)
            raise MjpegException(errors)
        return self
    def get(self):
        return None

# --- 
# /usr/local/lib/input_file.so [options]
# ---------------------------------------------------------------
# The following parameters can be passed to this plugin:
    # The following parameters can be passed to this plugin:
    # [-d | --delay ]........: delay (in seconds) to pause between frames
    # [-f | --folder ].......: folder to watch for new JPEG files
    # [-r | --remove ].......: remove/delete JPEG file after reading
    # [-n | --name ].........: ignore changes unless filename matches
    # [-e | --existing ].....: serve the existing *.jpg files from the specified directory
# ---------------------------------------------------------------
class MjpegFileIn(MjpegStreamerUtil):
    def __init__(self):
        super(MjpegFileIn,self).__init__()
        self.name = 'file-in'
        self.args.update({'i':'/usr/local/lib/mjpg-streamer/input_file.so','d':'unset','r':'unset','f':'unset','n':'unset','e':'unset'})
    def get(self):
        self.validate()
        return '%s'%(self.args.get('i'))

# --- https://github.com/jacksonliam/mjpg-streamer/blob/master/mjpg-streamer-experimental/plugins/input_uvc/README.md
# /usr/local/lib/input_uvc.so [options]
# ---------------------------------------------------------------
# The following parameters can be passed to this plugin:
    # [-d | --device ].......: video device to open (your camera)
    # [-r | --resolution ]...: the resolution of the video device,
    #                          can be one of the following strings:
    #                          QSIF QCIF CGA QVGA CIF VGA 
    #                          SVGA XGA SXGA 
    #                          or a custom value like the following
    #                          example: 640x480
    # [-q | --quality ] .....: set quality of JPEG encoding
    # [-f | --fps ]..........: frames per second
    #                          (activates YUYV format, disables MJPEG)
    # [-m | --minimum_size ].: drop frames smaller then this limit, useful
    #                          if the webcam produces small-sized garbage frames
    #                          may happen under low light conditions
    # [-e | --every_frame ]..: drop all frames except numbered
    # [-n | --no_dynctrl ]...: do not initalize dynctrls of Linux-UVC driver
    # [-l | --led ]..........: switch the LED "on", "off", let it "blink" or leave
    #                          it up to the driver using the value "auto"
    # [-t | --tvnorm ] ......: set TV-Norm pal, ntsc or secam
    # [-u | --uyvy ] ........: Use UYVY format, default: MJPEG (uses more cpu power)
    # [-y | --yuv  ] ........: Use YUV format, default: MJPEG (uses more cpu power)
    # [-fourcc ] ............: Use FOURCC codec 'argopt', 
    #                          currently supported codecs are: RGBP 
# ---------------------------------------------------------------
# Optional parameters (may not be supported by all cameras):
    # [-br ].................: Set image brightness (auto or integer)
    # [-co ].................: Set image contrast (integer)
    # [-sh ].................: Set image sharpness (integer)
    # [-sa ].................: Set image saturation (integer)
    # [-cb ].................: Set color balance (auto or integer)
    # [-wb ].................: Set white balance (auto or integer)
    # [-ex ].................: Set exposure (auto, shutter-priority, aperature-priority, or integer)
    # [-bk ].................: Set backlight compensation (integer)
    # [-rot ]................: Set image rotation (0-359)
    # [-hf ].................: Set horizontal flip (true/false)
    # [-vf ].................: Set vertical flip (true/false)
    # [-pl ].................: Set power line filter (disabled, 50hz, 60hz, auto)
    # [-gain ]...............: Set gain (auto or integer)
    # [-cagc ]...............: Set chroma gain control (auto or integer)
# ---------------------------------------------------------------
class MjpegUvcIn(MjpegStreamerUtil):
    def __init__(self):
        super(MjpegUvcIn,self).__init__()
        self.name = 'ucv'
        self.args.update({'i':'/usr/local/lib/mjpg-streamer/input_uvc.so','d':'unset','r':'768x432','f':'10'}) # -d /dev/video0
    def get(self):
        self.validate()
        return '%s -d %s -r %s -f %s\' -n -u -q 50'%(self.args.get('i'),self.args.get('d'),self.args.get('r'),self.args.get('f'))

# --- https://github.com/jacksonliam/mjpg-streamer/blob/master/mjpg-streamer-experimental/plugins/input_opencv/README.md
# /usr/local/lib/input_opencv.so [options]
# ---------------------------------------------------------------
# The following parameters can be passed to this plugin:
    # [-d | --device ].......: video device to open (your camera)
    # [-r | --resolution ]...: the resolution of the video device,
    #                          can be one of the following strings:
    #                          QQVGA QCIF CGA QVGA CIF VGA 
    #                          SVGA XGA HD SXGA UXGA FHD 
    #                          or a custom value like the following
    #                          example: 640x480
    # [-f | --fps ]..........: frames per second
    # [-q | --quality ] .....: set quality of JPEG encoding
# ---------------------------------------------------------------
# Optional parameters (may not be supported by all cameras):
    # [-br ].................: Set image brightness (integer)
    # [-co ].................: Set image contrast (integer)
    # [-sh ].................: Set image sharpness (integer)
    # [-sa ].................: Set image saturation (integer)
    # [-ex ].................: Set exposure (off, or integer)
    # [-gain ]...............: Set gain (integer)
# ---------------------------------------------------------------
# Optional filter plugin:
    # [ -filter ]............: filter plugin .so
    # [ -fargs ].............: filter plugin arguments
# ---------------------------------------------------------------
class MjpegOpencvIn(MjpegStreamerUtil):
    def __init__(self):
        super(MjpegOpencvIn,self).__init__()
        self.name = 'ocv-in'
        self.args.update({'i':'/usr/local/lib/mjpg-streamer/input_opencv.so','d':'unset','r':'640x480','f':'15'})
    def get(self):
        self.validate()
        return '%s -d %s -r %s -r %s -n -y'%(self.args.get('i'),self.args.get('d'),self.args.get('r'),self.args.get('f'))

# --- 
# /usr/local/lib/input_http.so [options]
# ---------------------------------------------------------------
# The following parameters can be passed to this plugin:
    # [-v | --version ]........: current SVN Revision
    # [-h | --help]............: show this message
    # [-H | --host]............: select host to data from, localhost is default
    # [-p | --port]............: port, defaults to 8080
# ---------------------------------------------------------------
class MjpegHttpIn(MjpegStreamerUtil):
    def __init__(self):
        super(MjpegHttpIn,self).__init__()
        self.name = 'http-in'
        self.args.update({'i':'/usr/local/lib/mjpg-streamer/input_opencv.so','h':'unset','p':'640x480'})
    def get(self):
        self.validate()
        return '%s -H %s -p %s'%(self.args.get('i'),self.args.get('h'),self.args.get('p'))

# --- https://github.com/jacksonliam/mjpg-streamer/blob/master/mjpg-streamer-experimental/plugins/input_raspicam/README.md
# /usr/local/lib/input_raspicam.so [options]
# ---------------------------------------------------------------
# The following parameters can be passed to this plugin:
    # [-fps | --framerate]...: set video framerate, default 5 frame/sec, max 30
    # [-x | --width ]........: width of frame capture, default 640, HD 1366
    # [-y | --height]........: height of frame capture, default 480, HD 768
    # [-quality].............: set JPEG quality 0-100, default 85
    # [-usestills]...........: uses stills mode instead of video mode
    # [-preview].............: enable full screen preview
    # ---------------------------------------------------------------
    # https://www.raspberrypi.org/app/uploads/2013/07/RaspiCam-Documentation.pdf
    # ---------------------------------------------------------------
    # [-sh]..................: Set image sharpness (-100 to 100)
    # [-co]..................: Set image contrast (-100 to 100)
    # [-br]..................: Set image brightness (0 to 100)
    # [-sa]..................: Set image saturation (-100 to 100)
    # [-ISO].................: Set capture ISO
    # [-vs]..................: Turn on video stabilisation
    # [-ev]..................: Set EV compensation
    # [-ex]..................: Set exposure mode (see raspistill notes)
    # [-awb].................: Set AWB mode (see raspistill notes)
    # [-ifx].................: Set image effect (see raspistill notes)
    # [-cfx].................: Set colour effect (U:V)
    # [-mm]..................: Set metering mode (see raspistill notes)
    # [-rot].................: Set image rotation (0-359)
    # [-stats]...............: Compute image stats for each picture (reduces noise)
    # [-drc].................: Dynamic range compensation level (see raspistill notes)
    # [-hf]..................: Set horizontal flip
    # [-vf]..................: Set vertical flip
# ---------------------------------------------------------------
# Optional parameters (may not be supported by all cameras):
    # [-sh]..................: Set image sharpness (-100 to 100)
    # [-co]..................: Set image contrast (-100 to 100)
    # [-br]..................: Set image brightness (0 to 100)
    # [-sa]..................: Set image saturation (-100 to 100)
    # [-ISO].................: Set capture ISO
    # [-vs]..................: Turn on video stabilisation
    # [-ev]..................: Set EV compensation
    # [-ex]..................: Set exposure mode (see raspistill notes)
    # [-awb].................: Set AWB mode (see raspistill notes)
    # [-ifx].................: Set image effect (see raspistill notes)
    # [-cfx].................: Set colour effect (U:V)
    # [-mm]..................: Set metering mode (see raspistill notes)
    # [-rot].................: Set image rotation (0-359)
    # [-stats]...............: Compute image stats for each picture (reduces noise)
    # [-drc].................: Dynamic range compensation level (see raspistill notes)
    # [-hf]..................: Set horizontal flip
    # [-vf]..................: Set vertical flip
# ---------------------------------------------------------------
class MjpegRaspiCamIn(MjpegStreamerUtil):
    def __init__(self):
        super(MjpegRaspiCamIn,self).__init__()
        self.name = 'rpi'
        self.args.update({'i':'/usr/local/lib/mjpg-streamer/input_raspicam.so','x':'1280','y':'720','q':'100','f':'15'})
    def get(self):
        self.validate()
        return '%s -x %s -y %s -quality %s -fps %s'%(self.args.get('i'),self.args.get('x'),self.args.get('y'),self.args.get('q'),self.args.get('f'))

# --- https://github.com/jacksonliam/mjpg-streamer/blob/master/mjpg-streamer-experimental/plugins/output_http/README.md
# /usr/local/lib/output_http.so [options]
# http://localhost:[PORT]
# ---------------------------------------------------------------
# The following parameters can be passed to this plugin:
    # [-w | --www ]...........: folder that contains webpages in 
    #                           flat hierarchy (no subfolders) /usr/local/www
    # [-p | --port ]..........: TCP port for this HTTP server
    # [-c | --credentials ]...: ask for "username:password" on connect easily sniffed and decoded, just base64 encoded
    # [-n | --nocommands ]....: disable execution of commands
# ---------------------------------------------------------------
# To access the stream using VLC, Firefox, Chrome:
    # ---
    # single input plugins
    # http://127.0.0.1:8080/?action=stream
    # ---
    # multiple input plugins
    # http://127.0.0.1:8080/?action=stream_0
    # http://127.0.0.1:8080/?action=stream_1
    # ---
    # capture a snapshot
    # http://127.0.0.1:8080/?action=snapshot
# ---------------------------------------------------------------
class MjpegHttpOut(MjpegStreamerUtil):
    def __init__(self):
        super(MjpegHttpOut,self).__init__()
        self.name = 'http-out'
        self.args.update({'o':'/usr/local/lib/mjpg-streamer/output_http.so','p':'8080','c':None,'w':'/root/pi.stalker/static/mjpg'})
    def get(self):
        self.validate()
        tmp = '%s -w %s -p %s -n'%(self.args.get('o'),self.args.get('w'),self.args.get('p'))
        if not None == self.args.get('c'):
            tmp = '%s -c %s'%(tmp,self.args.get('c'))
        return tmp

# --- https://github.com/jacksonliam/mjpg-streamer/blob/master/mjpg-streamer-experimental/plugins/output_viewer/README.md
# /usr/local/lib/output_viewer.so
# ---------------------------------------------------------------
class MjpegViewerOut(MjpegStreamerUtil):
    def __init__(self):
        super(MjpegViewerOut,self).__init__()
        self.name = 'viewer'
        self.args.update({'i':'/usr/local/lib/mjpg-streamer/output_viewer.so'})
    def get(self):
        self.validate()
        return '%s'%(self.args.get('i'))

# --- 
# /usr/local/lib/output_file.so
# ---------------------------------------------------------------
# The following parameters can be passed to this plugin:
    # [-f | --folder ]........: folder to save pictures
    # [-m | --mjpeg ].........: save the frames to an mjpg file 
    # [-l | --link ]..........: link the last picture in ringbuffer as this fixed named file
    # [-d | --delay ].........: delay after saving pictures in ms
    # [-i | --input ].........: read frames from the specified input plugin
# ---------------------------------------------------------------
# The following arguments are takes effect only if the current mode is not MJPG
    # [-s | --size ]..........: size of ring buffer (max number of pictures to hold)
    # [-e | --exceed ]........: allow ringbuffer to exceed limit by this amount
    # [-c | --command ].......: execute command after saving picture
# ---------------------------------------------------------------
class MjpegFileOut(MjpegStreamerUtil):
    def __init__(self):
        super(MjpegFileOut,self).__init__()
        self.name = 'file-out'
        self.args.update({'i':'/usr/local/lib/mjpg-streamer/output_file.so','f':'unset','d':'15000'})
    def get(self):
        self.validate()
        return '%s -f %s -d %s'%(self.args.get('i'),self.args.get('f'),self.args.get('d'))





# -------------------------------------------------------------------------------------------------
# https://www.raspberrypi.org/forums/viewtopic.php?t=77796
# -------------------------------------------------------------------------------------------------
# Usage: mjpg_streamer -i "[file|http|ucv|opencv|ptp2|raspicam]" -o "[file|http|udp|viewer]" [-b]
# -------------------------------------------------------------------------------------------------
    # [-i | --input  "<input-plugin.so> [parameters]"
    # [-o | --output "<output-plugin.so> [parameters]"
    # [-b | --background]...: fork to the background, daemon mode
# -------------------------------------------------------------------------------------------------
# Usage: mjpg_streamer [-h|-v]
# -------------------------------------------------------------------------------------------------
    # [-h | --help ]........: display this help
    # [-v | --version ].....: display version information
# -------------------------------------------------------------------------------------------------
class MjpegStream(object):
    def __init__(self):
        self.events = {'create-video':self.create,'kill-video':self.kill}
        self.args = {'emitter':None,'id':'video','label':'unset','in':'unset','out':'http-out','deamon':True}
        self.plugin = {'d':'unset','r':'unset','f':'unset'} # d /dev/video0
        self.plugout = {'w':'unset','p':'unset','c':None} # 'user:pass'
        self.input = {'ucv':MjpegUvcIn,'ocv':MjpegOpencvIn,'rpi':MjpegRaspiCamIn}
        self.output = {'http-out':MjpegHttpOut,'viewer':MjpegViewerOut}
        self.cmd = ['mjpg_streamer','-i',None,'-o',None]
        self.emitter = None
        self.process = None

    def decorate(self,arguments):
        if 'emitter' in arguments.keys():
            arguments.get('emitter').attach(self.events)
        akeys = self.args.keys()
        ikeys = self.plugin.keys()
        okeys = self.plugout.keys()
        for key in arguments:
            if key in akeys:
                self.args[key] = arguments[key]
            if key in ikeys:
                self.plugin[key] = arguments[key]
            if key in okeys:
                self.plugout[key] = arguments[key]
        return self

    def create(self,data={}):
        self.emitter = self.args.get('emitter')
        try:
            if not None == self.process:
                raise MjpegException(['alredy running, call kill before start'])
            tmp = self.args.get('in')
            if tmp in self.input.keys():
                self.cmd[2] = self.input.get(tmp)().decorate(self.plugin).get()
            tmp = self.args.get('out')
            if tmp in self.output.keys():
                self.cmd[4] = self.output.get(tmp)().decorate(self.plugout).get()
            if(self.args.get('deamon')):
                self.cmd.append('-b')
            if 'unset' == self.args.get('label'):
                self.args['label'] = '%s-%s'%(self.args.get('in'),tmp)
            for val in self.cmd:
                if(None == val or 'None' in val):
                    raise MjpegException(['illegal arguments. %s'%(str(self.cmd))])
            from subprocess import Popen, PIPE
            self.process = Popen(self.cmd,stdout=PIPE,stdin=PIPE,stderr=PIPE)
            logging.debug('%s: %s video stream started from %s (pid=%s)'%(self.args.get('label'),self.args.get('out'),self.args.get('in'),self.process.pid+2))
            logging.debug(self.process.stderr.read().replace('\n',''))
            deamon = {'pid':self.process.pid+2,'host':'0','port':0}
            if 'http-out' == self.args.get('out'):
                from netifaces import ifaddresses, AF_INET
                host = str(ifaddresses('wlan0')[AF_INET][0]['addr'])
                port = self.plugout.get('p')
                deamon['host'] = host
                deamon['port'] = port
                logging.debug('access stream on port %s:%s, %s'%(host,port,self.plugout.get('c')))
                self.emitter.emit('video-created',{'call':'video-created','id':'create-video','label':self.args.get('label'),'port':port,'credentials':self.plugout.get('c')})
            # add to hells kitchen
            from Process import ProcessDeamon
            ProcessDeamon().create().update(self.args.get('label'),deamon,True).write()
            from time import sleep
            sleep(0.1)
        except MjpegException as e:
            logging.error(e.toString())
        return self

    def kill(self,data={}):
        if(not None == self.process):
            pid = self.process.pid+2
            label = self.args.get('label')
            from os import system
            system('kill -9 %s'%(pid))
            logging.debug('%s to %s video stream %s (%s) stopped'%(self.args.get('out'),self.args.get('in'),label,pid))
            self.process.kill()
            self.process.terminate()
            self.process = None
            # reset hells kitchen
            from Process import ProcessDeamon
            ProcessDeamon().create().update(self.args.get('label')).write()
            self.emitter.emit('video-killed',{'call':'video-killed','id':'kill-video','label':label})
        return self
# -------------------------------------------------------------------------------------------------
# motion camera streaming                    https://www.lavrsen.dk/foswiki/bin/view/Motion/WebHome
# -------------------------------------------------------------------------------------------------
# screen resolution list                https://pacoup.com/2011/06/12/list-of-true-169-resolutions/
# -------------------------------------------------------------------------------------------------
    #      w      h  mod 8  16:9                                                           comments
    #    384    216     Y     Y                                                      extremely tiny
    #    512    288     Y     Y                                 very nice on wlan despite downloads
    #    640    360     Y     Y
    #    768    432     Y     Y
    #    896    504     Y     Y
    #   1024    576     Y     Y
    #   1152    648     Y     Y
    #   1280    720     Y     Y    720p HD
    #   1408    792     Y     Y
    #   1536    864     Y     Y
    #   1664    936     Y     Y
    #   1792   1008     Y     Y
    #   1920   1080     Y     Y   1080p HD
    #   2048   1152     Y     Y
# -------------------------------------------------------------------------------------------------
# sudo modprobe bcm2835-v4l2 or 
# add bcm2835-v4l2 to /etc/modules ! makes pi cam visible in /dev/video*
# -------------------------------------------------------------------------------------------------
# sudo service motion start
# sudo service motion stop
# sudo service motion status
# -------------------------------------------------------------------------------------------------
# /etc/default/motion
# -------------------------------------------------------------------------------------------------
    # start_motion_daemon=yes
# -------------------------------------------------------------------------------------------------
# /etc/motion/motion.conf
    # http://192.168.178.174:8080/0/config/list
    # http://192.168.178.174:8080/0/config/set
    # http://192.168.178.174:8080/0/config/get
    # http://192.168.178.174:8080/0/action/snapshot
    # http://192.168.178.174:8080/0/action/restart
    # -------------------------------------------------------------------------------------------------
    # deamon on
    # ??? webcontrol_localhost on|off
    # ??? webcontrol_html_output on|off
    # ffmpeg_output_movies off
    # ffmpeg_output_debug_movies off
    # output_debug_pictures off
    # output_pictures off
    # target_dir /home/pi/Monitor
    # v4l2_palette 15
    # width %d
    # height %d
    # framerate %d
    # stream_quality 50
    # stream_maxrate 100
    # stream_localhost off
    # -------------------------------------------------------------------------------------------------
    # mkdir /home/pi/Monitor
    # sudo chgrp motion /home/pi/Monitor
    # chmod g+rwx /home/pi/Monitor
# -------------------------------------------------------------------------------------------------
class MotionStream(object):
    pass
# ------------------------------------------------------------------------------------------------------
# picamera web streaming     https://picamera.readthedocs.io/en/release-1.13/recipes2.html#web-streaming
# ------------------------------------------------------------------------------------------------------
class PiStream(object):
    pass
# -------------------------------------------------------------------------------------------------
# flask camera streaming            https://blog.miguelgrinberg.com/post/video-streaming-with-flask
#                                   https://github.com/miguelgrinberg/flask-video-streaming
# -------------------------------------------------------------------------------------------------
class FlaskStream(object):
    def __init__(self):
        self.running = False
        self.thread = None
        self.frame = None
        from picamera import PiCamera
        self.camera = PiCamera()

    def create(self,data={}):
        if self.running:
            logging.warning('flask stream already started')
            return self
        self.thread = threading.Thread(target=self.stream)
        self.thread.start()
        return self

    def frame(self):
        if not self.running:
            raise Exception()
        timeout = time.time()
        # wait until frames start to be available
        # cancel on timeout
        while None == self.frame:
            time.sleep(1)
            if 5 > time.time()-timeout:
                raise Exception()
        return self.frame

    def stream(self):
        self.running = True
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True
            camera.start_preview() # let camera warm up
            time.sleep(2)
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # store frame
                stream.seek(0)
                self.frame = stream.read()
                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

class Cameras(object):
    def __init__(self):
        self.events = {'create-cameras':self.create,'kill-cameras':self.kill}
        self.args = {'emitter':None}
        from random import randint
        self.paths = {}
        self.ports = {}
        import platform
        # load driver
            # sudo modprobe bcm2835-v4l2
            # autoload driver on boot
            # sudo nano /etc/modules
            # bcm2835-v4l2
        if 'arm' == platform.machine():
            self.environment = 'raspberry'
            self.paths = {'frontcam':'/dev/video0'}
            self.ports = {'frontcam':randint(8000,8079)}
        else:
            self.environment = 'desktop'
            self.paths = {'frontcam':'/dev/video0'     ,'backcam':'/dev/video2'     ,'sidecam':'/dev/video4'}
            self.ports = {'frontcam':randint(8000,8079),'backcam':randint(8000,8079),'sidecam':randint(8000,8079)}
        self.streams = []

    def decorate(self,arguments):
        if 'emitter' in arguments.keys():
            arguments.get('emitter').attach(self.events)
        keys = self.paths.keys()
        akey = self.args.keys()
        for key in arguments.keys():
            if key in akey:
                self.args[key] = arguments[key]
            if key in keys:
                rec = arguments.get(key)
                tmp = rec.keys()
                if 'p' in tmp:
                    self.ports[key] = rec['p']
                if 'd' in tmp:
                    self.paths[key] = rec['d']
        return self

    def create(self,data={}):
        from glob import glob
        cams = glob('/dev/video*')
        keys = self.paths.keys()
        vals = self.paths.values()
        port = self.ports.values()
        emit = self.args.get('emitter')
        for cam in cams:
            if cam in vals:
                index = vals.index(cam)
                self.streams.append(MjpegStream().decorate({'emitter':emit,'label':keys[index],'d':cam,'p':port[index],'in':'ucv'}).create())
        return self

    def kill(self,data={}):
        for stream in self.streams:
            stream.kill()
        return self