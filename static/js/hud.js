function HtmlCancasTool(animation){ /* used in animation.X.js move ? */
	var holder = animation;
    this.canvasParse = (id) => {
        return document.getElementById(id);
    }
    this.canvasScroll = () => {
    	// wrap canvas to scroll container
        var canvas = document.createElement("canvas");
        var scroll = document.createElement("scroll");
        scroll.appendChild(canvas);
        if('body' === holder.setting.args.paneParent){
        	document.body.appendChild(scroll)
        } else {
            var element = document.getElementById(holder.setting.args.paneParent);
            element.insertBefore(scroll, element.childNodes[0])
        }
        return canvas;
    }
    this.canvasCreate = () => {
        var canvas = document.createElement("canvas");
        if('body' === holder.setting.args.paneParent){
            document.body.appendChild(canvas);
        } else {
            var element = document.getElementById(holder.setting.args.paneParent);
            element.insertBefore(canvas, element.childNodes[4]);
        }
        return canvas;
    }
}



/* crosshairs */
function DotCrosshair(animation){
    var holder = animation;
    this.name = 'dot';
    this.push = function(){
        context = holder.objects.ctxm;
        context.fillStyle = holder.setting.args.lineColor;
        x = holder.setting.args.paneWidth/2;
        y = holder.setting.args.paneHeight/2;
        r = 2;
        return this;
    }
    var context = null;
    var x = 0;
    var y = 0;
    var r = 0;
    this.update = function() {
        context.beginPath();
        context.arc(x,y,r,0,2*Math.PI);
        context.fill();
        context.closePath();
    }
}

function DriveCrosshair(animation){
    var holder = animation;
    this.name = 'drive';
    this.push = function(){
        context = holder.objects.ctxm;
        context.strokeStyle = holder.setting.args.lineColor;
        context.fillStyle = holder.setting.args.lineColor;
        x = holder.setting.args.paneWidth/2;
        y = holder.setting.args.paneHeight/2;
        r = holder.setting.args.paneHeight*0.2;
        return this;
    }
    var context = null;
    var x = 0;
    var y = 0;
    var r = 0;
    this.update = function() {
        context.beginPath(); 
        context.arc(x,y,r,0,2*Math.PI); /* circle */
        context.stroke();
        context.closePath();

        context.beginPath(); 
        context.arc(x,y,2,0,2*Math.PI); /* dot */
        context.fill();

        context.moveTo(x-r*4/5,y); /* left wing */
        context.lineTo(x-2*r*4/5,y);
        context.stroke();

        context.moveTo(x+r*4/5,y); /* right wing */
        context.lineTo(x+2*r*4/5,y);
        context.stroke();
        context.closePath();
    }
}



/* main animation code */
function HudInterfaceValidation(animation){
    var holder = animation;
    this.holder = () => {
        try{
            var errors = []
            if(!holder.objects){errors.push('Objects Holder not found!');}
            if(!holder.operator){errors.push('Operator not found!');}
            if(!holder.engine){errors.push('Engine not found!');}
            if(!holder.setting){errors.push('Setting not found!');}
            if(0 < errors.length){throw errors}
        }catch(error){
            console.error(error);
        }
    }
    this.objects = () => {
        try{
            var errors = []
            if(!holder.objects.main){errors.push('Pane not found!');}
            if(!holder.objects.ctxm){errors.push('context not found!');}
            if(0 < errors.length){throw errors}
        }catch(error){
            console.error(error);
        }
    }
    this.any = () => {
        this.holder();
        this.objects();
    }
}
function HudInterfaceEngine(animation){
    var holder = animation;
    var canvas = null;
    var context = null;
    this.start = function(){
        context = holder.objects.ctxm;
        canvas = holder.objects.main;
        this.push();
        stopFlag = false;
        this.stopped = false;
        update();
    }
    this.pause = function(){
    	stopFlag = true;
    	this.stopped = true;
    }
    this.resume = function(){
    	stopFlag = false;
    	this.stopped = false;
    	update();
    }
    this.push = function(){
        holder.objects.crosshair.push();
    }
    var stopFlag = true;
    this.stopped = true;
    function update() {
    	context.clearRect(0,0,canvas.width,canvas.height);
        holder.objects.crosshair.update();
        if(!stopFlag){
            window.requestAnimationFrame(update);
        }
    }
}
function HudInterfaceSetting(){
    this.rad = 2 * Math.PI;
    this.args = {
       'paneParent':'body'
       ,'paneInject':'unset'
       ,'paneId':'hud-if-'+(Math.random()*(99999-10000)+10000)
       ,'paneColor':'rgba(0,0,0,0)'
       ,'paneWidth':window.innerWidth
       ,'paneHeight':window.innerHeight
       ,'paneBorder':0
       ,'lineColor':'rgba(0,0,0,1)'
       ,'lineWidth':'2px'
       ,'crosshair':'drive'
    }
    this.decorate = function(opts){
        for(var key in opts){
            if(this.args.hasOwnProperty(key)){
                this.args[key] = opts[key];
            }
        }
        return this;
    }
}
function HudInterfaceOperator(animation){
    var holder = animation;
    holder.operator = this;
    this.decorate = function(opts){
        holder.setting.decorate(opts);
        return this;
    }
    this.create = function(dispatcher){
        holder.listener.create(dispatcher);
    	/* main pane*/
    	holder.objects.main = holder.util.canvasCreate();
        canvas = holder.objects.main;
        canvas.id = holder.setting.args.paneId+'-main';
        canvas.width = holder.setting.args.paneWidth;
        canvas.height = holder.setting.args.paneHeight;
        holder.objects.ctxm = canvas.getContext("2d");
	 	
        if('drive' == holder.setting.args.crosshair){holder.objects.crosshair = new DriveCrosshair(holder);}
        else if('dot' == holder.setting.args.crosshair){holder.objects.crosshair = new DotCrosshair(holder);}
        else{holder.objects.crosshair = new DotCrosshair(holder);}

        return this;
    }
    this.validate = function(){
        return this;
    }
    this.start = function(){
    	holder.engine.pause();
        holder.engine.start();
        return this;
    }
    this.pause = function(){
        holder.engine.pause();
        return this;
    }
    this.resume = function(){
        holder.engine.resume();
        return this;
    }
    this.toggle = function(){
    	var stopped = holder.engine.stopped;
    	if(stopped){holder.engine.resume();}
    	else{holder.engine.pause();}
        return stopped;
    }
    this.change = function(data){
        if('dot' == holder.objects.crosshair.name){
            holder.objects.crosshair = new DriveCrosshair(holder).push();
        } else if('drive' == holder.objects.crosshair.name){
            holder.objects.crosshair = new DotCrosshair(holder).push();
        }
    }
    this.tint = function(data){
        holder.setting.args.lineColor = data.color;
        holder.objects.crosshair.push();
    }
}
function HudInterfaceListener(animation){
    var holder = animation;
    var events = {
        'decorate-hud-if':(data) => {holder.operator.decorate(opts);}
       ,'create-hud-if':(data) => {holder.operator.create(data.dispatcher);}
       ,'switch-hud-if':(data) => {holder.operator.change(data);}
       ,'tint-hud-if':(data) => {holder.operator.tint(data);}
    }
    this.create = function(dispatcher){
        if(dispatcher){
            dispatcher.append({'events':Object.keys(events),'issues':Object.values(events)})
        }
    }
    }
function HudInterfaceObjects(){
	this.main = null;
	this.ctxm = null;
    this.crosshair = null;
}
function HudInterfaceHolder(){
    this.listener = new HudInterfaceListener(this);
    this.objects = new HudInterfaceObjects();
    this.operator = new HudInterfaceOperator(this);
	this.engine = new HudInterfaceEngine(this);
    this.setting = new HudInterfaceSetting();
    this.validate = new HudInterfaceValidation(this);
    this.util = new HtmlCancasTool(this);
} 