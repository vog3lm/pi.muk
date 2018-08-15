import logging

class GpioException(Exception):
    def __init__(self,errors):
        self.errors = errors
    def toString(self):
        return ' '.join(self.errors) # str(self.errors).replace('\'','').replace('[','').replace(']','')

class GpioDummy(object):
    def __init__(self):
        self.args = {'mode':'BCM'}
        self.bcm = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0
                   ,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0
                   ,21:0,22:0,23:0,24:0,25:0,26:0,27:0}
        self.setup = {}
        self.board = {}
        for key in range(0,40):
            self.board[key] = 0
        self.mode = {}

    def setmode(self,mode):
        if 'GPIO.BCM' == mode:
            self.mode = self.bcm
        elif 'GPIO.BOARD' == mode:
            self.mode = self.board

    def setwarnings(self,val):
        pass

    def setup(self,key,val,initial=0):
        self.setup[key] = val
        self.board[key] = initial

    def output(self,key,val):
        self.mode[key] = val

    def input(self,key):
        return self.mode[key]

    def cleanup(self):
        pass

# ---------------------------------------------------------------
# Rapsberry Pi 3/Zero BCM
# ---------------------------------------------------------------
    #            +3V3 [ ] [ ] +5V
    #  SDA1 / GPIO  2 [ ] [ ] +5V
    #  SCL1 / GPIO  3 [ ] [ ] GND
    #         GPIO  4 [ ] [ ] GPIO 14 / TXD0
    #             GND [ ] [ ] GPIO 15 / RXD0
    #         GPIO 17 [ ] [ ] GPIO 18
    #         GPIO 27 [ ] [ ] GND
    #         GPIO 22 [ ] [ ] GPIO 23
    #            +3V3 [ ] [ ] GPIO 24
    #  MOSI / GPIO 10 [ ] [ ] GND
    #  MISO / GPIO  9 [ ] [ ] GPIO 25
    #  SCLK / GPIO 11 [ ] [ ] GPIO  8 / CE0#
    #             GND [ ] [ ] GPIO  7 / CE1#
    # ID_SD / GPIO  0 [ ] [ ] GPIO  1 / ID_SC
    #         GPIO  5 [ ] [ ] GND
    #         GPIO  6 [ ] [ ] GPIO 12
    #         GPIO 13 [ ] [ ] GND
    #  MISO / GPIO 19 [ ] [ ] GPIO 16 / CE2#
    #         GPIO 26 [ ] [ ] GPIO 20 / MOSI
    #             GND [ ] [ ] GPIO 21 / SCLK
# ---------------------------------------------------------------
# Rapsberry Pi 3/Zero BOARD
# ---------------------------------------------------------------
    #         +3V3  1 [ ] [ ]  2 +5V
    #  SDA1 / GPIO  3 [ ] [ ]  4 +5V
    #  SCL1 / GPIO  5 [ ] [ ]  6 GND
    #         GPIO  7 [ ] [ ]  8 GPIO 14 / TXD0
    #          GND  9 [ ] [ ] 10 GPIO 15 / RXD0
    #         GPIO 11 [ ] [ ] 12 GPIO 18
    #         GPIO 13 [ ] [ ] 14 GND
    #         GPIO 15 [ ] [ ] 16 GPIO 23
    #         +3V3 17 [ ] [ ] 18 GPIO 24
    #  MOSI / GPIO 19 [ ] [ ] 20 GND
    #  MISO / GPIO 21 [ ] [ ] 22 GPIO 25
    #  SCLK / GPIO 23 [ ] [ ] 24 GPIO  8 / CE0#
    #          GND 25 [ ] [ ] 26 GPIO  7 / CE1#
    # ID_SD / GPIO 27 [ ] [ ] 28 GPIO  1 / ID_SC
    #         GPIO 29 [ ] [ ] 30 GND
    #         GPIO 31 [ ] [ ] 32 GPIO 12
    #         GPIO 33 [ ] [ ] 34 GND
    #  MISO / GPIO 35 [ ] [ ] 36 GPIO 16 / CE2#
    #         GPIO 37 [ ] [ ] 38 GPIO 20 / MOSI
    #          GND 39 [ ] [ ] 40 GPIO 21 / SCLK
# ---------------------------------------------------------------
class Gpios(object):
    def __init__(self):
        self.args = {'emitter':None,'warn':False} # mode:GPIO.BOARD|GPIO.BCM
        self.events = {'create-gpio':self.create,'kill-gpio':self.kill}
        self.emitter = None

    def decorate(self,arguments):
        from Process import decorate
        return decorate(self,arguments)

    def create(self,data={}):
        self.emitter = self.args.get('emitter')
        try:
            import RPi.GPIO as GPIO
            self.gpio = GPIO
            self.gpio.setmode(GPIO.BCM)
        except ImportError as e:
            logging.error('pi gpio import failed %s'%(str(e)))
            self.gpio = GpioDummy()
            self.gpio.setmode('GPIO.BCM')
            logging.warning('pi gpio dummy initialized')
        self.gpio.setwarnings(self.args.get('warn'))
        logging.info('pi gpio initialized as BCM')
        self.emitter.emit('gpio-created',{'id':'create-gpio','call':'gpio-created','gpio':self.gpio})
        return self

    def register(self,data):
        # self.gpio.setup(7,GPIO.OUT) # out:0|in:1 initial=0
        # response self.gpio
        # GPIO.output(7, 1) #Set TRIG as HIGH
        # GPIO.output(7, 0) #Set TRIG as LOW
        # GPIO.input(7)==0: #Check whether the 7 is LOW
        # GPIO.input(7)==1: #Check whether the 7 is HIGH
        return self

    def kill(self,data={}):
        self.gpio.cleanup()
        logging.info('gpios cleaned.')
        self.emitter.emit('gpio-killed',{'id':'kill-gpio','call':'gpio-killed'})
        return self



