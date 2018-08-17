
function Gamepad4p1Operator(){
	const gamepad = new Gamepad();
	var state = 'destroyed';
	var events = {
		'toggle-gamepad':() => {
			if('paused'){
				gamepad.resume();
				state = 'started'
			}else{
				gamepad.pause();
				state = 'paused'
			}
		}
	}
	this.create = function(dispatcher){
		if(dispatcher){
			dispatcher.append({'events':Object.keys(events),'issues':Object.values(events)})
		}
	}
	this.start = function(dispatcher){
		gamepad.on('press','button_1',() => { /* A */
		    console.log('a','was pressed!');
		});
		gamepad.on('release','button_1',() => { /* A */
		    console.log('a','was released!');
		});
		gamepad.on('press','button_2',() => { /* B */
		    console.log('b','was pressed!');
		});
		gamepad.on('release','button_2',() => { /* B */
		    console.log('b','was released!');
		});
		gamepad.on('press','button_3',() => { /* X */
		    console.log('x','was pressed!');
		});
		gamepad.on('release','button_3',() => { /* X */
		    console.log('x','was released!');
		});
		gamepad.on('press','button_4',() => { /* Y */
		    console.log('Y','was pressed!');
		});
		gamepad.on('release','button_4',() => { /* Y */
		    console.log('Y','was released!');
		});



		gamepad.on('press','shoulder_top_left',() => { /* L1 */
		    $('body').trigger('send-drive',{'call':'send-drive','id':'gamepad-tl','token':'idToken','request':'drive-remote','key':'L1','value':1});
		});
		gamepad.on('release','shoulder_top_left',() => { /* L1 */
		    $('body').trigger('send-drive',{'call':'send-drive','id':'gamepad-tl','token':'idToken','request':'drive-remote','key':'L1','value':0});
		});
		gamepad.on('press','shoulder_top_right',() => { /* R1 */
		    $('body').trigger('send-drive',{'call':'send-drive','id':'gamepad-tl','token':'idToken','request':'drive-remote','key':'R1','value':1});
		});
		gamepad.on('release','shoulder_top_right',() => { /* R1 */
		    $('body').trigger('send-drive',{'call':'send-drive','id':'gamepad-tl','token':'idToken','request':'drive-remote','key':'R1','value':0});
		});
		gamepad.on('press','shoulder_bottom_left',() => { /* L2 */
		    $('body').trigger('send-drive',{'call':'send-drive','id':'gamepad-tl','token':'idToken','request':'drive-remote','key':'L2','value':1});
		});
		gamepad.on('release','shoulder_bottom_left',() => { /* L2 */
		    $('body').trigger('send-drive',{'call':'send-drive','id':'gamepad-tl','token':'idToken','request':'drive-remote','key':'L2','value':0});
		});
		gamepad.on('press','shoulder_bottom_right',() => { /* R2 */
		    $('body').trigger('send-drive',{'call':'send-drive','id':'gamepad-tl','token':'idToken','request':'drive-remote','key':'R2','value':1});
		});
		gamepad.on('release','shoulder_bottom_right',() => { /* R2 */
		    $('body').trigger('send-drive',{'call':'send-drive','id':'gamepad-tl','token':'idToken','request':'drive-remote','key':'R2','value':0});
		});
		//	gamepad.on('hold','shoulder_bottom_axis',(e) => { /* L2 *//* hold -> value */
		//		/* 	is not used, drive or not drive */
		//	    console.log('LR2','was hold!',e.value);
		//	});



		gamepad.on('press','stick_button_left',() => { /* TL */
		    $('body').trigger('send-drive',{'call':'send-drive','id':'gamepad-tl','token':'idToken','request':'drive-remote','key':'TL','value':1});
		});
		//	gamepad.on('release','stick_button_left',() => { /* TL */
		//	    console.log('TL','was shoot!');
		//	});
		gamepad.on('press','stick_button_right',() => { /* TR */
		    $('body').trigger('send-drive',{'call':'send-drive','id':'gamepad-tl','token':'idToken','request':'drive-remote','key':'TR','value':1});
		});
		//	gamepad.on('release','stick_button_right',() => { /* TR */
		//	    console.log('TR','was snapshot!');
		//	});



		gamepad.on('press','select',() => { /* select */
		    console.log('select','was pressed!');
		});
		gamepad.on('release','select',() => { /* select */
		    console.log('select','was released!');
		});
		gamepad.on('press','start',() => { /* start */
		    console.log('start','was pressed!');
		});
		gamepad.on('release','start',() => { /* start */
		    console.log('start','was released!');
		});



		//	gamepad.on('press','stick_axis_left',() => { /* joysick left */
		//	    console.log('stick_axis_left','was pressed!');
		//	});
		//	gamepad.on('release','stick_axis_left',() => { /* joysick left */
		//	    console.log('stick_axis_left','was released!');
		//	});
		gamepad.on('hold','stick_axis_left',(e) => { /* joysick left */
		    console.log('stick_axis_left','was hold!',e.value);
		    // values : [-1,0] tower left
		    //		  : [ 1,0] tower right
		    //		  : [0,-1] tower up
		    //		  : [0, 1] tower down
		});
		//	gamepad.on('press','stick_axis_right',() => { /* joystick right */
		//	    console.log('stick_axis_right','was pressed!');
		//	});
		//	gamepad.on('release','stick_axis_right',() => { /* joystick right */
		//	    console.log('stick_axis_right','was released!');
		//	});
		gamepad.on('hold','stick_axis_right',(e) => { /* joystick right */
		    console.log('stick_axis_right','was hold!',e.value);
		    // values : [-1,0] gimbal left
		    //		  : [ 1,0] gimbal right
		    //		  : [0,-1] gimbal up
		    //		  : [0, 1] gimbal down
		});



		gamepad.on('press','d_pad_axis',(e) => { /* hat/cross *//* do not hold! */
		    var x = e.value[0];
		    var y = e.value[1];
		    if(-1 == x){ /*left*/ $('body').trigger('toggle-mirror',{});}
		    else if (-1 == y){ /*up*/ $('body').trigger('switch-cameras',{});}
		    else if (1 == y){ /*down*/ $('body').trigger('switch-hud-if',{});}
		    else if (1 == x){ /*right*/}
		});
	}

	this.kill = function(){
		gamepad.destroy();
	}

	gamepad.on('connect', e => {
	    this.start();
	    state = 'started';
	});
	gamepad.on('disconnect', e => {
		console.log('disconnect',e)
	    gamepad.off('press', 'button_1');
	    gamepad.off('release', 'button_1');
	    gamepad.off('press', 'button_2');
	    gamepad.off('release', 'button_2');
	    gamepad.off('press', 'button_3');
	    gamepad.off('release', 'button_3');
	    gamepad.off('press', 'button_4');
	    gamepad.off('release', 'button_4');
	    gamepad.off('press', 'shoulder_top_left');
	    gamepad.off('release', 'shoulder_top_left');
	    gamepad.off('press', 'shoulder_top_right');
	    gamepad.off('release', 'shoulder_top_right');
	    gamepad.off('press', 'shoulder_bottom_left');
	    gamepad.off('release', 'shoulder_bottom_left');
	    gamepad.off('press', 'shoulder_bottom_right');
	    gamepad.off('release', 'shoulder_bottom_right');
	    gamepad.off('press', 'stick_button_left');
	    gamepad.off('release', 'stick_button_left');
	    gamepad.off('press', 'stick_button_right');
	    gamepad.off('release', 'stick_button_right');
	    self.sate = 'destroyed';
	});
}

function Keyboard4p1Operator(){
	var events = {
		'toggle-keyboard':() => {

		}
	}
	this.create = function(dispatcher){
		if(dispatcher){
			dispatcher.append({'events':Object.keys(events),'issues':Object.values(events)})
		}
	}
	this.start = function(){

	}
	this.kill = function(){

	}
}

function Drive4p1Operator(){
	var driver = null;
	var args = {'driver':'gamepad'}
	var events = {
		'drive-connected':(data) => {driver.start();}
		,'drive-disconnected':(data) => {driver.kill();}
	}
    this.decorate = function(opts){
        for(var key in opts){
            if(args.hasOwnProperty(key)){
                args[key] = opts[key];
            }
        }
        return this;
    }
	this.create = function(dispatcher){
		if(dispatcher){
			dispatcher.append({'events':Object.keys(events),'issues':Object.values(events)});
		}
		if('keyboard' == args.driver){
			driver = new Gamepad4p1Operator();
		} else if('gamepad' == args.driver){
			driver = new Keyboard4p1Operator();
		}
		driver.create(dispatcher);
	}
}