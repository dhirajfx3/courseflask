var va;
var runn=false;
function add_e(e,val)
{
	if(val=="")
		return;
	var c=document.createElement('text');
	c.innerHTML=val;
	c.setAttribute("class",'L');
	e.parent().parent().children().eq(1).append(c);
	e.parent().parent().find('.box').get(0).scrollTop=e.parent().parent().find('.box').get(0).scrollHeight-300;
	//	e.parent().find('.box').scrollTop(e.parent().find('.box').scrollHeight()-300);
}
function execute(socket)
{
$(".sender2").keyup(function(event){
		if(event.keyCode == 13){
        $(".send").click();}});
			$('.send').click(function(){
			var msg=$(this).parent().children().eq(0).val();
			$(this).parent().children().eq(0).val("");
			var obj={};
			obj['from']=$('#curr').val();
			obj['to']=$(this).parent().parent().attr('id');
			obj['msg']=msg;
			socket.emit('json',obj);
			add_e($(this),msg);
		});
		$('.above_box').click(function()
		{
			if(runn)
				window.clearInterval(va);
			runn=false;
			$('title').html($('#curr').val());
			$(this).find('.just').find('.title').css('backgroundColor','rgba(214,63,214,0.5)');
			$(this).find('.just').find('.title').css('-webkit-box-shadow', '0px 0px 0px 0px rgba(147,238,245,1)');
			//$(this).css('background-color','rgba(214,63,214,0.5)');
		});
}
function create(name,socket)
{
	var x=document.createElement('div');
	x.setAttribute("class",'above_box');
	x.setAttribute('id',name);
	var y=document.createElement('div');
	y.setAttribute('class','just');
	var text=document.createElement('text');
	text.setAttribute('class','title');
	text.innerHTML=name;
	y.appendChild(text);
	var f=document.createElement('div');
	f.setAttribute('class','box');
	var h=document.createElement('div');
	h.setAttribute('class','sender');
	var uiin=document.createElement('input');
	uiin.setAttribute('type','text');
	uiin.setAttribute('size','20');
	uiin.setAttribute('class','sender2');
	uiin.setAttribute('placeholder','Enter text here');
	var but=document.createElement('button');
	but.setAttribute('class','send');
	but.innerHTML='Send';
	h.appendChild(uiin);
	h.appendChild(but);
	x.appendChild(y);
	x.appendChild(f);
	x.appendChild(h);
	document.body.appendChild(x);
	execute(socket);
}
function add_e_L(e,val)
{
	if(val=="")
		return;
	var c=document.createElement('text');
		c.setAttribute("class",'R');
		c.innerHTML=val;
	var fd=document.getElementById(e).childNodes;
	for ( var x = 0;x<fd.length;x++)
		if(fd[x].className=='box')
		{
			fd[x].appendChild(c);
			var z=fd[x].scrollHeight;
			fd[x].scrollTop=z-300;
			break;
		}
}
function e1()
{
		$(this).css('-webkit-box-shadow', '0px 0px 40px 15px rgba(147,238,245,1)');
		$(this).css('backgroundColor', 'white');
}
function e2()
{
		$(this).css('-webkit-box-shadow', '0px 0px 0px 0px rgba(147,238,245,1)');
		$(this).css('background-color','rgba(214,63,214,0.5)');
}
var j=0;
function blink(ele,frm,to)
{
	if(j%2==0)
	{
		document.getElementsByTagName('title')[0].innerHTML=frm.split('@')[0]+" messaged you";
		ele.style.webkitBoxShadow= '0px 0px 40px 15px rgba(147,238,245,1)';
		ele.style.backgroundColor= 'white';
			++j;
	}
	else if(j)
	{
		document.getElementsByTagName('title')[0].innerHTML=to;
		ele.style.webkitBoxShadow= '0px 0px 0px 0px rgba(147,238,245,1)';
		ele.style.backgroundColor='rgba(214,63,214,0.5)';
			++j;
	}
}
$(document).ready(function() {
	 var socket = io.connect(document.domain + ':' + location.port);
	 execute(socket); 
		socket.on('incoming_text',function(dat)
		{
			if($('#curr').val()==dat.to&&dat.msg!="")
			{
				if(document.getElementById(dat.from))
				{
					;
				}
				else
				{
				create(dat.from,socket);
				}
				add_e_L(dat.from,dat.msg);
				if(runn==false)
				va = window.setInterval(function()
				{
					var z=document.getElementById(dat.from).childNodes;
					var s=0;
					for(s=0;z[s].className!='just';s++);
					z=z[s].childNodes;
					for(s=0;z[s].className!='title';s++);
					blink(z[s],dat.from,dat.to);
					runn=true;
					;},1000);
			}
		});
		
		$('.title').hover(
		function()
		{
			$(this).css('-webkit-box-shadow', '0px 0px 40px 15px rgba(147,238,245,1)');
			$(this).css('backgroundColor', 'white');
		},
		function()
		{
			$(this).css('-webkit-box-shadow', '0px 0px 0px 0px rgba(147,238,245,1)');
			$(this).css('background-color','rgba(214,63,214,0.5)');
		}
		);
		});