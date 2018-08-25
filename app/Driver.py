import logging

class MouseDriver(object):
    def __init__(self):
        self.args = {'emitter':None,'gpio':None}
        self.events = {'create-mouse-driver':self.create,'kill-mouse-driver':self.kill,'gpio-created':self.decorate}
        self.name = 'mouse-driver'
        self.args = {'lib':'inputs'}

    def create(self):
        return self

    def inputs(self):
        pass

    def pynput(self):
        pass

class KeyboardDriver(object):
    def __init__(self):
        self.args = {'emitter':None,'gpio':None}
        self.events = {'create-keyboard-driver':self.create,'kill-keyboard-driver':self.kill,'gpio-created':self.decorate}
        self.name = 'keyboard-driver'
        self.keymap = {}
        self.keys = []
        self.thread = None
        self.running = False

    def create(self,data={}):
        self.running = False
        from pynput.keyboard import Controller, Listener, Key, KeyCode
        Controller()
        self.keymap = {Key.left:self.dummy
                      ,Key.up:self.dummy
                      ,Key.right:self.dummy
                      ,Key.down:self.dummy
                      ,Key.space:self.dummy
                      ,'w':self.dummy
                      ,'a':self.dummy
                      ,'s':self.dummy
                      ,'d':self.dummy}
        self.keys = self.keymap.keys()
        self.thread = Listener(on_press=self.press,on_release=self.release)
        self.running = True
        self.thread.start()
        #self.thread.join()
        return self

    # available keys in Key
        # ,'f1','f10','f11','f12','f13','f14','f15','f16','f17','f18','f19','f2','f20','f3','f4','f5','f6','f7','f8','f9'
        # ,'alt_gr','alt_l','alt_r','backspace','caps_lock','cmd','cmd_r' ,'ctrl','ctrl_r','delete','end','enter','esc'
        # ,'home','insert','menu','num_lock','page_down','page_up','pause','print_screen','scroll_lock','shift','shift_r','space','tab'
        # ,'left','right','down','up','space'
        # ,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
        # ,'a,'b,'c,'d,'e,'f,'g,'h,'i,'j,'k,'l,'m,'n,'o,'p,'q,'r,'s,'t,'u,'v,'w,'x,'y,'z'
    def press(self,key):
        if key in self.keys:
            self.keymap.get(key)(True)
        elif hasattr(key,'char'):
            if(key.char in self.keys):
                self.keymap.get(key.char)(True)            
        return self.running

    def release(self,key):
        if key in self.keys:
            self.keymap.get(key)(False)
        elif hasattr(key,'char'):
            if(key.char in self.keys):
                self.keymap.get(key.char)(False)  
        return self.running

    def kill(self,data={}):
        self.running = False
        return self

    def dummy(self,pressed):
        print 'dummy'

class GamepadDriver(object):
    def __init__(self):
        self.args = {'emitter':None,'gpio':None}
        self.events = {'create-gamepad-driver':self.create,'kill-gamepad-driver':self.kill,'gpio-created':self.decorate}
        self.name = 'gamepad-driver'
        self.keymap = {}
        self.keys = []
        self.thread = None
        self.running = False
        self.gamepad = None
        self.gpio = None

    def decorate(self,arguments):
        from Process import decorate
        return decorate(self,arguments)

    def create(self,data={}):
        self.running = False
        self.keymap = {'BTN_TL':self.accel_rev_left
                      ,'BTN_TR':self.accel_rev_right
                      ,'BTN_TL2':self.accel_fwd_left
                      ,'BTN_TR2':self.accel_fwd_right
                      ,'ABS_Z':self.tower_x
                      ,'ABS_RZ':self.tower_y
                      ,'ABS_X':self.gimbal_x
                      ,'ABS_Y':self.gimbal_y}
        self.keys = self.keymap.keys()
        try:
            from inputs import get_gamepad
            self.gamepad = get_gamepad
        except IOError as e:
            self.gamepad = None
            logging.error('inputs missing. call pip install inputs')

        errors = []
        if None == self.gamepad:
            errors.append('no gamepad hardware connected')
        if None == self.args.get('gpio'):
            errors.append('gamepad-driver has no gpio hardware interface')
        if 0 < len(errors):
            logging.error('gamepad-driver not startable.')
            logging.error(' '.join(errors))
            return self
        self.gpio = self.args.get('gpio')
        self.gpio.setup(19,0,initial=0) # out:0|in:1
        self.gpio.setup(26,0,initial=0)
        self.gpio.setup(20,0,initial=0)
        self.gpio.setup(21,0,initial=0)
        from threading import Thread
        self.thread = Thread(target=self.inputs)
        self.thread.setDaemon(True) # self.args.get('deamon')
        self.thread.start()
        logging.debug('gamepad-driver has been started')
        logging.debug('BTN_L1 -> accel rev left')
        logging.debug('BTN_R1 -> accel rev right')
        logging.debug('BTN_L2 -> accel fwd left')
        logging.debug('BTN_L2 -> accel fwd right')
        logging.debug('JOY_RX -> horizontal tower rotation')
        logging.debug('JOY_RY -> vertical tower rotation')
        logging.debug('JOY_RT -> canon shoot')
        logging.debug('JOY_LX -> horizontal gimbal rotation')
        logging.debug('JOY_LY -> vertical gimbal rotation')
        logging.debug('JOY_LT -> gimbal camera snapshot')
        return self

    def inputs(self):
        self.running = True
        while self.running:
            events = self.gamepad()
            for event in events:
                # stick actions
                    # ABS_X = left x [0,128,255] left to right
                    # ABS_Y = left y [0,128,255] up to down
                    # ABS_Z = right x [0,128,255] left to right
                    # ABS_RZ = right y [0,128,255] up to down
                # hat actions
                    # ABS_HAT0X == cross x [-1,1] left, right
                    # ABS_HAT0Y == cross y [-1,1] up, down
                # button actions
                    # BTN_SOUTH == a
                    # BTN_EAST == b
                    # BTN_NORTH == x
                    # BTN_WEST == y
                    # BTN_TL == l1 [0,1]
                    # BTN_TR == r1
                    # BTN_TL2 == l2b [0,1]
                    # BTN_TR2 == r2b [0,1]
                    # ABS_BRAKE == l2m [0,255]
                    # ABS_GAS == r2m [0,255]
                    # BTN_THUMBL == l3 [0,1]
                    # BTN_THUMBR == r3 [0,1]
                    # ABS_SELECT == select
                    # ABS_START == start
                self.running = self.handler(event.code,event.state)
        logging.debug('gampad driver has been stopped')

    def kill(self,data={}):
        self.running = False
        return self

    def handler(self,key,value):
        if key in self.keys:
            self.keymap.get(key)(value)
        return self.running
    # ---------------------------------------------------------------
    # Rapsberry Pi 3/Zero BCM
    # ---------------------------------------------------------------
        #            +3V3 [ ] [ ] +5V
        #               2 [ ] [ ] +5V
        #               3 [ ] [ ] GND
        #               4 [ ] [ ] 14
        #             GND [ ] [ ] 15
        #              17 [ ] [ ] 18
        #              27 [ ] [ ] GND
        #              22 [ ] [ ] 23
        #            +3V3 [ ] [ ] 24
        #              10 [ ] [ ] GND
        #               9 [ ] [ ] 25
        #              11 [ ] [ ]  8
        #             GND [ ] [ ]  7
        #               0 [ ] [ ]  1
        #               5 [ ] [ ] GND
        #               6 [ ] [ ] 12
        #              13 [ ] [ ] GND
        #    lr engine 19 [ ] [ ] 16
        #    lf engine 26 [ ] [ ] 20 engine rr
        #             GND [ ] [ ] 21 engine rf
    # ---------------------------------------------------------------
    def accel_fwd_left(self,value):
        self.gpio.output(26,value)

    def accel_fwd_right(self,value):
        self.gpio.output(21,value)

    def accel_rev_left(self,value):
        self.gpio.output(19,value)

    def accel_rev_right(self,value):
        self.gpio.output(20,value)

    def tower_x(self,value):
        print 'gimbal move rotate %s'%(float(value-128)/128)

    def tower_y(self,value):
        print 'gimbal move up down %s'%(float(value-128)/128)

    def gimbal_x(self,value):
        print 'gimbal move x %s'%(float(value-128)/128)

    def gimbal_y(self,value):
        print 'gimbal move y %s'%(float(value-128)/128)

    def shoot(self,value):
        print 'shoot'

    def snapshot(self,value):
        print 'shoot'

class RemoteDriver(object):
    def __init__(self):
        self.args = {'emitter':None,'gpio':None}
        self.events = {'create-remote-driver':self.create,'gpio-created':self.decorate,'drive-remote':self.handler}
        self.name = 'remote-driver'
        self.keymap = {}
        self.keys = {}
        self.gpio = None

    def decorate(self,arguments):
        from Process import decorate
        return decorate(self,arguments)

    def create(self,data={}):
        self.keymap = {'L1':self.accel_rev_left
                      ,'R1':self.accel_rev_right
                      ,'L2':self.accel_fwd_left
                      ,'R2':self.accel_fwd_right
                      ,'TL':self.shoot
                      ,'TR':self.snapshot
                      ,'ABS_Z':self.tower_x
                      ,'ABS_RZ':self.tower_y
                      ,'ABS_X':self.gimbal_x
                      ,'ABS_Y':self.gimbal_y}
        self.keys = self.keymap.keys()

        if None == self.args.get('gpio'):
            logging.error('gamepad-driver not startable.')
            logging.error('gamepad-driver has no gpio hardware interface')
            return self
        self.gpio = self.args.get('gpio')
        self.gpio.setup(19,0,initial=0) # out:0|in:1
        self.gpio.setup(26,0,initial=0)
        self.gpio.setup(20,0,initial=0)
        self.gpio.setup(21,0,initial=0)

        logging.debug('remote-driver has been started')
        logging.debug('L1 -> accel rev left')
        logging.debug('R1 -> accel rev right')
        logging.debug('L2 -> accel fwd left')
        logging.debug('L2 -> accel fwd right')
        #logging.debug('RX -> horizontal tower rotation')
        #logging.debug('RY -> vertical tower rotation')
        logging.debug('RT -> canon shoot')
        #logging.debug('LX -> horizontal gimbal rotation')
        #logging.debug('LY -> vertical gimbal rotation')
        logging.debug('LT -> gimbal camera snapshot')

        return self

    def handler(self,data):
        if None == self.gpio:
            logging.error('remote driver error. gpio not set')
            return self
        keys = data.keys()
        if not 'key' in keys or not 'value' in keys:
            logging.error('remote driver error. no key or value found')
        key = data.get('key')
        if key in self.keys:
            self.keymap.get(key)(data.get('value'))
        return self

    # ---------------------------------------------------------------
    # Rapsberry Pi 3/Zero BCM
    # ---------------------------------------------------------------
        #            +3V3 [ ] [ ] +5V
        #               2 [ ] [ ] +5V
        #               3 [ ] [ ] GND
        #               4 [ ] [ ] 14
        #             GND [ ] [ ] 15
        #              17 [ ] [ ] 18
        #              27 [ ] [ ] GND
        #              22 [ ] [ ] 23
        #            +3V3 [ ] [ ] 24
        #              10 [ ] [ ] GND
        #               9 [ ] [ ] 25
        #              11 [ ] [ ]  8
        #             GND [ ] [ ]  7
        #               0 [ ] [ ]  1
        #               5 [ ] [ ] GND
        #               6 [ ] [ ] 12
        #              13 [ ] [ ] GND
        #    lr engine 19 [ ] [ ] 16
        #    lf engine 26 [ ] [ ] 20 engine rr
        #             GND [ ] [ ] 21 engine rf
    # ---------------------------------------------------------------
    def accel_fwd_left(self,value):
        self.gpio.output(26,value)

    def accel_fwd_right(self,value):
        self.gpio.output(21,value)

    def accel_rev_left(self,value):
        self.gpio.output(19,value)

    def accel_rev_right(self,value):
        self.gpio.output(20,value)

    def tower_x(self,value):
        print 'gimbal move rotate %s'%(float(value-128)/128)

    def tower_y(self,value):
        print 'gimbal move up down %s'%(float(value-128)/128)

    def gimbal_x(self,value):
        print 'gimbal move x %s'%(float(value-128)/128)

    def gimbal_y(self,value):
        print 'gimbal move y %s'%(float(value-128)/128)

    def shoot(self,value):
        print 'shoot'

    def snapshot(self,value):
        print 'snapshot'

