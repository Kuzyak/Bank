var AdoElement=function(a){var c=this;this.loadingLib=false;this.buff=ado.placeholder;this.tmpBuff="";this.config=a;this.onLoad=a.onLoad;this.DOMElement={};this.DOMElementBufor="";this.regs={scriptBegin:/^\s*<script\b((?:\s+[\w_:][-\w_.:]*\s*(?:=\s*(?:\"[^\"]*\"|\'[^\']*\'|[^\s\"\'>][^\s>]*))?)*)[^\w>]*>/i,scriptEnd:/(<\/script(?![\w:.-])[^>]*>)/i,attr:/([\w:][-\w.:]*(?![-\w.:]))(?:\s*=\s*(?:\"([^\"]*)\"|\'([^\']*)\'|([^\s\"\'>][^\s>]*)))?/g};this.myWrite=function(e){c.tmpBuff+=e};this.myWriteln=function(e){c.myWrite(e+"\n")};this.isMaster=function(){return this.config.master};this.isSlave=function(){return this.config.slave};this.initBuffor=function(){ado.busy=true;window.document.open=function(){};window.document.close=function(){};document.write=c.myWrite;document.writeln=c.myWriteln};this.rewriteBuffor=function(){if(this.buff.indexOf(ado.placeholder)!==-1){this.buff=c.buff.replace(ado.placeholder,c.tmpBuff)}else{this.buff=this.tmpBuff+this.buff}this.tmpBuff=""};this.preDispatch=function(){if(typeof this.config!=="object"){return}if(!this.config.id||!this.config.server){return}if(ado.protocol.substr(0,4)!=="http"){return}this.getDOMElement();this.emptyDOMElement();this.DOMElementBufor="";if(!this.isSlave()){if(this.config.preview){this.config.url=this.config.server}else{this.makeUrl()}}this.appendRedirUrl();if(ado.mode==="old"||!ado.isBrowserSupport()){document.write("<script type='text/javascript' src='"+c.config.url+"'><\/script>");if(typeof a.onLoad==="function"){a.onLoad=false}}else{this.initBuffor();this.appendScript(this.config.url,null,true)}};this.postDispatch=function(){this.flushDOMBufor();ado.busy=false;ado.start()};var d=function(e){if(typeof e.defer!="undefined"){return false}var g="";if(e.language){g=e.language.toLowerCase()}var f="";if(e.type){f=e.type.split(";")[0]}if(g=="vbscript"||/\/vbscript$/i.test(f)){return false}return true};this.dispatch=function(){this.deleteComment();var f;var g=this;if(this.regs.scriptBegin.test(this.buff)){f=this.regs.scriptBegin.exec(this.buff);var e=this.processAttributes(f[1]);if(!d(e)){this.skipScript(f)}else{if(e.src){this.processSrcScript(f,e.src,e.charset)}else{this.processInlineScript(f)}}}else{var k=function(){if(g.DOMElement){g.addToDOMElement(g.buff.replace(ado.placeholder,""));g.buff=""}if(typeof g.config.onLoad==="function"){g.onLoad();g.onLoad=false}g.postDispatch()};if(!this.regs.scriptBegin.test(this.buff)){var j=/<script/i;f=j.exec(this.buff);if(f){var h=this.buff.indexOf(f[0]);this.DOMElement=ado.getById(this.config.id);if(this.DOMElement){this.addToDOMElement(this.buff.substr(0,h).replace(ado.placeholder,""))}this.buff=this.buff.substr(h);this.dispatch()}else{k()}}}return};this.deleteComment=function(){var e=/\<!\s*--(.*?)(--\s*\>)/m;while(e.test(c.buff)){c.buff=c.buff.replace(e,"")}};this.skipScript=function(e){var f=this.regs.scriptEnd.exec(c.buff);td_flashinstalled=2;td_browserFlashversion=8;this.buff=ado.placeholder+this.buff.substr(f.index+f[0].length);c.dispatch()};this.processSrcScript=function(e,g,h){this.buff=c.buff.substr(e[0].length);var f=this.regs.scriptEnd.exec(c.buff);this.buff=ado.placeholder+this.buff.substr(f.index+f[0].length);this.appendScript(g,h)};this.appendScript=function(g,j,e,h){var f=function(k){c.loadingLib=false;if(typeof h==="function"){h()}c.rewriteBuffor();c.dispatch()};this.loadingLib=true;ado.loadScript(g,f,j);return};this.onServerEmission=function(){var g=function(){if(typeof c.config.onServerEmissionEmpty==="function"){c.config.onServerEmissionEmpty()}};if(typeof adserver_emissions2==="object"){var f=0;for(var e in adserver_emissions2){if(typeof adserver_emissions2[e]!=="function"){f++}}if(f>ado.adserverEmissions){ado.adserverEmissions++;if(typeof c.config.onServerEmission==="function"){c.config.onServerEmission()}}else{g()}}else{g()}};this.processInlineScript=function(e){if(c.loadingLib){return}this.buff=this.buff.substr(e[0].length);var h=this.regs.scriptEnd.exec(c.buff);var g=this.buff.substr(0,h.index);this.buff=ado.placeholder+this.buff.substr(h.index+h[0].length);g=g.replace("/*<![CDATA[*/","");g=g.replace("<![CDATA[","");g=g.replace("/* <![CDATA[ */","");g=g.replace("/* ]]> */","");g=g.replace("/*]]>*/","");g=g.replace("<!--","");g=g.replace("//-->","");g=g.replace("//]]>-->","");g=g.replace(/\/\*.*\*\//g,"");try{ado.evaluate(g)}catch(f){}this.rewriteBuffor();this.dispatch();return};this.processAttributes=function(f){var e={};var h;while(h=c.regs.attr.exec(f)){var g=null;if(h[4]){g=h[4]}else{if(h[3]){g=h[3]}else{if(h[2]){g=h[2]}}}e[h[1].toLowerCase()]=g}return e};this.getDOMElement=function(){this.DOMElement=ado.getById(this.config.id);if(!this.DOMElement){return}};this.emptyDOMElement=function(){if(this.DOMElement){this.DOMElement.innerHTML="";this.DOMElement.style.display="none"}};this.flushDOMBufor=function(){this.insertToDOMElement(this.DOMElementBufor);this.DOMElementBufor=""};this.addToDOMElement=function(e){this.DOMElementBufor+=e};this.insertToDOMElement=function(e){if(this.DOMElement&&e!==""){this.DOMElement.style.display="block";this.DOMElement.innerHTML=e}};this.makeUrl=function(){if(this.config.preview){this.config.server=this.config.emiter}var e=this.config.contentType;switch(e){case"txt":case"xml":case"js":break;default:e="js";break}this.config.url=ado.protocol+"//"+this.config.server;this.config.url+="/_"+(new Date()).getTime()+"/ad."+e+"?id="+ado.trimAdoPrefix(this.config.orgId)+"/x="+screen.width+"/y="+screen.height;this.config.url+=ado.makeKeywords(this.config.keys)+ado.makeVars(this.config.vars);this.config.url+=ado.makeCluster(this.config.clusters)+ado.makeFlash();return};this.appendRedirUrl=function(){if(this.config.redir&&this.config.redir!==""&&this.config.redir!="<%%REDIR%%>"){this.config.url=this.config.url+"/redir="+this.config.redir}}};var AdoContainer=function(){var that=this;var userAgent=navigator.userAgent.toLowerCase();var tuneId=function(config){config.orgId=config.id;config.id=config.id+""+ado.iterator++;var de=ado.getById(config.orgId);if(de){de.id=config.id}return config};var keywordEncode=function(s){var d="";var k=0;var c="";if(!s){return}for(k=0;k<s.length;k++){c=s.charCodeAt(k);if(c<128){d+=s.charAt(k)}else{if(c>=128&&c<=2047){d+=String.fromCharCode(((c>>6)&31)|192,(c&63)|128)}else{d+=String.fromCharCode((c>>12)|224,((c>>6)&63)|128,(c&63)|128)}}}return escape(d).replace(/\//g,"%2F").replace(/\@/g,"%40").replace(/\*/g,"%2A").replace(/\+/g,"%2B").replace(/\%/g,"$")};this.elems=[];this.urlsMapping=[];this.masterSlaves=[];this.queue=[];this.iterator=0;this.busy=false;this.placeholder="__MARKER__";this.mode="old";this.characterEncoding=true;this.xml=false;this.previewUrl="";this.previewEnabled=[];this.tmp=[];this.adserverEmissions=0;this.windowLoad=false;this.protocol="";this.browser={version:(userAgent.match(/.+(?:rv|it|ra|ie)[\/: ]([\d.]+)/)||[])[1],safari:/webkit/.test(userAgent),opera:/opera/.test(userAgent),msie:/msie/.test(userAgent)&&!/opera/.test(userAgent),mozilla:/mozilla/.test(userAgent)&&!/(compatible|webkit)/.test(userAgent)};this.config=function(cfg){this.mode=cfg.mode;this.xml=cfg.xml;this.characterEncoding=cfg.characterEncoding;if(cfg.protocol){this.protocol=cfg.protocol}else{this.protocol=location.protocol}};this.resolvId=function(id,soft){for(var i in ado.elems){var cfg=ado.elems[i].config;if(cfg){if(soft){if(cfg.orgId===id||cfg.orgId==="ado-"+id){return i}}else{if((cfg.orgId===id||cfg.orgId==="ado-"+id)&&ado.elems[i].begin===false){return i}}}}return false};this.addAdoPrefix=function(config){if(config.id.length===46){config.id="ado-"+config.id}return config};this.trimAdoPrefix=function(orgId){if(orgId.length==46){return orgId}else{if(orgId.indexOf("ado-")===0){return orgId.substring(4,50)}else{return orgId}}};this.beginCreative=function(config){var tmp=this.elems[ado.resolvId(config.id,true)];if(tmp){tmp.onServerEmission()}return tmp};this.beginExternal=function(){};this.endExternal=function(){};this.refresh=function(id){var elem=ado.elems[ado.resolvId(id,true)];if(elem.isMaster()){ado.master(elem.config);this.masterSlaves[elem.config.orgId]=[];for(var i in ado.elems){if(typeof ado.elems[i]==="object"&&ado.elems[i].config.slave&&ado.elems[i].config.myMaster===elem.config.orgId){var config=ado.elems[i].config;ado.elems[i].emptyDOMElement();ado.slave(config.orgId,config)}}}else{ado.placement(elem.config);ado.start()}};this.placement=function(config){if(!config.id||!config.server){return}if(!config.orgId){config=tuneId(config)}var test=(ado.mode=="new"&&!ado.windowLoad&&this.isBrowserSupport());if((ado.mode=="new"&&!ado.windowLoad&&this.isBrowserSupport())||ado.busy){ado.queue.unshift(function(){ado.placement(config)});return}if(ado.previewEnabled[ado.protocol+"//"+config.server]){config.preview=true;config.server=ado.previewUrl+"?id="+ado.trimAdoPrefix(config.orgId)}this.elems[config.id]=new AdoElement(config);if(!ado.elems[config.id].DOMElement){return}this.elems[config.id].preDispatch()};this.master=function(config){config.master=true;if((ado.mode=="new"&&!ado.windowLoad&&this.isBrowserSupport())||ado.busy){ado.queue.unshift(function(){ado.master(config)});return}if(!config.orgId){config=tuneId(config)}if(typeof this.masterSlaves[config.orgId]==="undefined"){this.masterSlaves[config.orgId]=[]}this.elems[config.id]=new AdoElement(config);if(ado.previewEnabled[ado.protocol+"//"+config.server]){config.preview=true;config.server=ado.previewUrl+"?id="+ado.trimAdoPrefix(config.orgId)}this.elems[config.id].preDispatch()};this.slave=function(fnName,config){if(!fnName||typeof fnName!=="string"||fnName===""){return}if(!config||!config.myMaster){return}if(!config.id){config.id=fnName}config.slave=true;if((ado.mode=="new"&&!ado.windowLoad&&this.isBrowserSupport())||ado.busy){ado.queue.unshift(function(){ado.slave(fnName,config)});return}if(typeof this.masterSlaves[config.myMaster]!=="object"){this.masterSlaves[config.myMaster]=[]}this.masterSlaves[config.myMaster].push(fnName);if(!config.orgId){config=tuneId(config)}this.elems[config.id]=new AdoElement(config);this.elems[config.id].getDOMElement();this.elems[config.id].emptyDOMElement();if(ado.mode==="old"||!this.isBrowserSupport()){document.write("<script type='text/javascript'>if(typeof "+config.orgId+"=='function'){"+config.orgId+"();}<\/script>");if(typeof config.onLoad==="function"){config.onLoad();config.onLoad=false}}else{this.slaveStart(config)}};this.slaveStart=function(config){if(typeof globalScope[config.orgId]=="function"){eval(config.orgId)}this.elems[config.id].buff='<script type="text/javascript">if(typeof '+config.orgId+"=='function'){"+config.orgId+"();}<\/script>";this.elems[config.id].begin=false;this.elems[config.id].initBuffor();this.elems[config.id].dispatch()};this.preview=function(config){if(config.enabled===false){return}config.server=config.emiter;if(config.preview!==true){config.url=ado.protocol+"//"+config.server+"/_"+(new Date()).getTime()+"/ad.js?id="+config.id}if(!config.orgId){config=tuneId(config)}if(ado.mode=="new"&&!ado.windowLoad&&ado.isBrowserSupport()){ado.queue.unshift(function(){ado.preview(config)});return}if(ado.mode=="old"){document.write('<script src="'+config.url+'"><\/script>')}else{this.elems[config.id]=new AdoElement(config);this.elems[config.id].preDispatch()}};this.turnOnPreview=function(){for(var i in ado.tmp){if(typeof ado.previewEnabled[ado.tmp[i]]!=="function"){ado.previewEnabled[ado.tmp[i]]=true}}ado.tmp=[]};this.turnOffPreview=function(){for(var i in ado.previewEnabled){if(typeof ado.previewEnabled[i]!=="function"){if(ado.previewEnabled[i]){ado.tmp.push(i)}ado.previewEnabled[i]=false}}};this.getByTag=function(n,i){if(!i){i=0}var objs=ado.getAllByTag(n);return objs[i]};this.getAllByTag=function(n){var objs=[];if(document.all){objs=document.all.tags(n)}else{if(document.getElementsByTagName){objs=document.getElementsByTagName(n)}else{if(document.layers){objs=document.layers[n]}}}return objs};this.bind=function(elem,eventName,fn){if(elem.addEventListener){elem.addEventListener(eventName,fn,false)}else{if(elem.attachEvent){elem.attachEvent("on"+eventName,fn)}else{if(document.getElementById){}}}};this.isBrowserSupport=function(){return(document.createElement&&document.appendChild&&document.getElementById)?true:false};this.evaluate=function(code){if(window.execScript){window.execScript(code);return null}var result=globalScope.eval?globalScope.eval(code):eval(code);return result};this.loadScript=function(url,callback,charset){var done=false;var script=document.createElement("script");var indexOf=url.indexOf("javascript:");if(url.indexOf("javascript:")!==-1){var fn=url.substr(indexOf);ado.evaluate(fn);callback(this);return}var onload=function(){if(!done&&(!this.readyState||this.readyState=="loaded"||this.readyState=="complete")){done=true;callback(this)}};if(ado.browser.msie){script.onreadystatechange=onload}else{script.onload=onload}script.src=url;if(typeof charset!=="undefined"&&charset!==null){script.charset=charset}if(ado.browser.msie&&ado.loadingPreviewSettings){ado.onDOMReady(function(){ado.head.appendChild(script)})}else{if(ado.busy&&script.src.indexOf("redot.js")!=-1){if(ado.browser.msie){script.onreadystatechange=function(){}}else{script.onload=function(){}}setTimeout(function(){onload()},1)}ado.head.appendChild(script)}};this.makeKeywords=function(keys){var addNuggaddKey=function(keys){if(typeof na_prof==="string"){if(keys===""){keys="/key="}else{keys+=","}keys+=na_prof}return keys};if(typeof keys==="string"){keys=keys.split(",")}var k="";if(typeof keys==="object"&&keys.length>0){for(var key in keys){if(typeof keys[key]==="string"){if(ado.characterEncoding){k+=","+keywordEncode(keys[key].toLowerCase())}else{k+=","+keys[key].toLowerCase()}}}k="/key="+k.slice(1)}k=addNuggaddKey(k);return k};this.makeVars=function(vars){var v="";if(typeof vars==="object"){for(var key in vars){if(typeof vars[key]==="string"||typeof vars[key]==="number"){v+="/"+key+"="+vars[key]}}}else{if(typeof vars==="string"){if(vars.charAt(0)!=="&"){vars="&"+vars}if(vars.charAt(vars.length-1)==="&"){vars=vars.substr(0,vars.length-1)}vars=vars.replace("&","/");while(vars.indexOf("&")!==-1){vars=vars.replace("&","/")}v=vars}}return v};this.makeCluster=function(o){var t=this;this.a={1:"1000000000000000000",2:"2000000000000000000",3:"4000000000000000000",4:"8000000000000000000",5:"6100000000000000000",6:"2300000000000000000",7:"4600000000000000000",8:"8210000000000000000",9:"6520000000000000000",10:"2150000000000000000",11:"4201000000000000000",12:"8402000000000000000",13:"6904000000000000000",14:"2918000000000000000",15:"4836100000000000000",16:"8672300000000000000",17:"6355600000000000000",18:"2701310000000000000",19:"4412620000000000000",20:"8824250000000000000",21:"6758401000000000000",22:"2517902000000000000",23:"4034914000000000000",24:"8068838000000000000",25:"6127776100000000000",26:"2344553300000000000",27:"4688017600000000000",28:"8277124310000000000",29:"6545348620000000000",30:"2190786350000000000",31:"4281473701000000000",32:"8463847412000000000",33:"6927694924000000000",34:"2954399858000000000",35:"4819689717100000000",36:"8638379534300000000",37:"6376749178600000000",38:"2743598347310000000",39:"4496097784720000000",40:"8883185579450000000",41:"6777261159901000000",42:"2555523209912000000",43:"4011156408934000000",44:"8022203906978000000",45:"6144406812957100000",46:"2388802734815300000",47:"4667714478630700000",48:"8235538847370410000",49:"6560176794741820000",50:"2131243599492650000",51:"4262486099985211000",52:"8425863189971522000",53:"6940737269953054000",54:"2990474529917009000",55:"4891849058934108100",56:"8693698107978206300",57:"6397297304957502700",58:"2785585708815114410",59:"4471171516730328820",60:"8843243032570646750",61:"6796486064051292511",62:"2593963129003485032",63:"4097837248106861164"};this.c="";this.res=function(n,v){var p=[],m=[];for(i in v){if(v.hasOwnProperty(i)){if(v[i]<0){m.push(-v[i])}else{p.push(v[i])}}}return"/ADD_"+n+"="+t.conv(p)+"/REM_"+n+"="+t.conv(m)};this.conv=function(ar){r=new t.wy();for(i in ar){if(ar.hasOwnProperty(i)){if(t.a[ar[i]]){r.add(t.a[ar[i]])}}}return r.get()};this.wy=function(){var s=this;this.value="0000000000000000000";this.add=function(n){var over=false;var tmp="";for(x=0;x<n.length;x++){var ww=parseInt(n.charAt(x))+parseInt(s.value.charAt(x));if(over){ww++;over=false}ww=""+ww;if(ww.length==2){over=true;ww=ww.charAt(1)}tmp+=ww}s.value=tmp};this.get=function(){var ww="";for(i=s.value.length-1;i>=0;i--){ww+=s.value.charAt(i)}wyn=/0*([1-9][0-9]*)/.exec(ww);return(wyn)?wyn[1]:"0"}};if(typeof o==="object"){for(b in o){if(o.hasOwnProperty(b)){this.c+=this.res(b,o[b])}}}return this.c};this.makeFlash=function(){var fv="-";var fo=null;eval('try { f=(d==top.document)?1:2; if (typeof top.document.referrer=="string") { ref=top.document.referrer } } catch(e) {f=3;}');eval('try { fv=navigator.plugins["Shockwave Flash"].description; } catch (e) {}');eval('if (typeof ActiveXObject!="undefined") { try { fo=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7"); } catch(e) { try { fo=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6"); fv="X"; fo.AllowScriptAccess="always"; } catch(e) { if (fv=="X") { fv="WIN 6,0,20,0"; }} try { fo=new ActiveXObject("ShockwaveFlash.ShockwaveFlash"); } catch(e) {} } if ((fv=="-" || fv=="X") && fo) { fv=fo.GetVariable("$version"); }}');return"/fv="+escape(fv)};this.getById=function(id){return document.getElementById(id)};this.onDOMReady=function(readyFn){var countStyleSheets=function(){var style=ado.getAllByTag("style");var links=ado.getAllByTag("link");var j=0;for(var i in links){if(links[i].rel==="stylesheet"){j++}}return style.length+j};function bindReady(){if(document.addEventListener&&!ado.browser.opera){document.addEventListener("DOMContentLoaded",readyFn,false);ado.windowLoad=true;return}else{if(ado.browser.msie&&window==top){(function(){if(ado.windowLoad){return}try{document.documentElement.doScroll("left")}catch(error){setTimeout(arguments.callee,1);return}readyFn();ado.windowLoad=true;return})()}else{if(ado.browser.opera){document.addEventListener("DOMContentLoaded",function(){if(ado.windowLoad){return}for(var i=0;i<document.styleSheets.length;i++){if(document.styleSheets[i].disabled){setTimeout(arguments.callee,0);return}}readyFn();ado.windowLoad=true;return},false)}else{if(ado.browser.safari){var numStyles;(function(){if(ado.windowLoad){return}if(document.readyState!="loaded"&&document.readyState!="complete"){setTimeout(arguments.callee,0);return}if(numStyles===undefined){numStyles=countStyleSheets()}if(document.styleSheets.length!=numStyles){setTimeout(arguments.callee,0);return}readyFn();ado.windowLoad=true;return})()}else{window.onload=readyFn;ado.windowLoad=true;return}}}}}bindReady()};this.closeLivePreview=function(){window.location=ado.previewDisableUrl+"?url="+encodeURIComponent(encodeURIComponent(window.location.href))};this.start=function(){if(ado.queue.length>0){var fn=ado.queue.pop();if(typeof fn==="function"){fn()}}}};if(typeof ado==="undefined"){ado=new AdoContainer();if(typeof ado.head==="undefined"){ado.head=ado.getByTag("head",0)}var go=function(){ado.windowLoad=true;ado.start()};if(window.addEventListener){window.addEventListener("load",go,true)}else{if(window.attachEvent){window.attachEvent("onload",go)}else{if(document.getElementById){window.onload=go}}}}var globalScope=this;