function Sock3tEv3ntD1spatch3r(ns){
	if(!ns){ns = 'sio';}
	var namespace = ns;
	var socketobj = null;
	var events = {};
	events['connect-'+ns] = (data) => {
		socketobj = io.connect(location.protocol+'//'+document.domain+':'+location.port+'/'+namespace);
        socketobj.on('connected', function(data) {
            $('body').trigger(namespace+'-connected',data);
        });
        socketobj.on('response', function(data) {
            //$('body').trigger(namespace+'-got',data)  
            $('body').trigger(data.data.call,data.data) ; 
        });
	}
	events['disconnect-'+ns] = (data) => {}
	events['send-'+ns] = (data) => {
        if(null == socketobj){console.error(namespace,'socket not connected.','call','connect-'+namespace,'before sending messages.');}
        else{socketobj.emit('request',Object.assign({},data, {'call':'request'}));}
    }

	this.create = function(dispatcher){
		if(dispatcher){
			dispatcher.append({'events':Object.keys(events),'issues':Object.values(events)})
		}
	}
};

function V13wEv3ntD1spatch3r(){
    var events = [];
    var issues = [];
    this.decorate = function(holder){
	    events = holder.events;
	    issues = holder.issues;
	    return this;
    }
    this.append = function(holder){
    	for(var i=0; i<holder.events.length; i++){
    		var key = holder.events[i];
			events.push(key);
			issues.push(holder.issues[i]);
    	}
    	return this;
    }
    this.register = function(){
    	if(null == events || null == issues || 0 == events.length || 0 == issues.length){
    		throw 'view event dispachter not decorated. call onDecorate/onAppend first!'
    		return this;
    	}
		for (var i=0; i<events.length; i++) {
            $('body').on(events[i],dispatch);
        };
        return this;
    }
    this.unleash = function(){
        $("img").each(function(){ // make images clickable
            var element = $(this)
            if(element.attr('call')){
                element.on('click',function(){
                    var tmp = $(this)
                    $('body').trigger(tmp.attr('call'),{call:element.attr('call'),id:element.attr('id'),url:tmp.attr('url')});
                });
            }
        });
        $("a").each(function(){ // make ankors clickable
            var element = $(this)
            if(element.attr('call')){
                element.on('click',function(){
                    var tmp = $(this)
                    $('body').trigger(tmp.attr('call'),{call:element.attr('call'),id:element.attr('id'),url:tmp.attr('url')});
                });
            }
        });
        $('form').keypress(function(e) {
            if (e.which == 13) {
                e.preventDefault();
                var element = $(this)               
                if(element.attr('call')){
                    $('body').trigger(element.attr('call'),{call:element.attr('call'),id:element.attr('id'),url:element.attr('url')});
                }
            }
        });
        return this;
    }
    function dispatch(evt,data){
        try {
	    	if(events == null || issues == null){
	    		throw 'view event dispachter not decorated. call decorate/append first!'
	    	}
            for(var i=0;i<events.length;i++){
                if(events[i] === evt.type){
                    issues[i](data);
                }
            }
        //    index = events.indexOf(evt.type)
        //    if(index < 0){
        //        throw 'view event intel not found!'
        //    }
        //    issues[index](data)
        } catch(error) {
        	$('body').trigger('loading-stop');
            console.error(error)
        }
    }
};