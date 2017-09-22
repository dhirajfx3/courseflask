from flask import *
import MySQLdb
from datetime import datetime
from os import path,system
from flask_socketio import SocketIO
from flask_socketio import send,emit
from datetime import timedelta
from pickle import dump,load
from werkzeug import secure_filename
from cryptography.fernet import Fernet
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.MIMEBase import MIMEBase
from threading import Thread
from Tkinter import *
c=MySQLdb.connect('localhost','labwork','labwork','project')
pointer=c.cursor()
app = Flask(__name__)
socketio=SocketIO(app)
app.secret_key="KAH3$7cfX03.1*!;)"
APP=Tk()
APP.geometry("500x600")
def mainloo():
		APP.mainloop()
		scrollbar = Scrollbar(APP)
		scrollbar.pack(side=RIGHT, fill=Y)

Thread(target=mainloo).start()
try:
	pointer.execute("create table login (name varchar(50) primary key,K varchar(500),password varchar(500))")
except:
	pass
tkin='s'
@app.route('/')
def homet():
	return render_template("index.html")
@app.route('/about/')
def about():
	return render_template("about/index.html")
@app.route('/slotsfilled/')
def filled():
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select * from slots where availability='filled'")
	z=pointer.fetchall()
	return render_template("slots/slotsfilled.html",data=z)
@app.route('/slotsavail/')
def avail():
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select * from slots where availability='avail'")
	z=pointer.fetchall()
	#return str(z)
	return render_template("slots/slotsfilled.html",data=z)
@app.route('/contform',methods=["POST"])
def flakes():
	def funcT(mail):
		fr=open("sender.txt",'r').read()
		password=open('reader.txt','r').read()
		object=SMTP('smtp.gmail.com:587')
		object.starttls()
		object.login(fr,password)
		l=[mail];
		msg={'From':fr,'To':l[0],'Subject':'Do not Reply'}
		mine_mime=MIMEMultipart()
		text=MIMEText('Hello {0} !!!\n Your Query has been successfully submitted\n Thanks For Your Response'.format(l[0]),'plain')
		mine_mime.attach(text)
		for z in msg.keys():
			mine_mime[z]=msg[z]
		msg=mine_mime.as_string()
		object.sendmail(fr,l[0],msg);
		print("Send to"+str(mail))
		object.quit()
	Thread(target=funcT,args=(request.form['mail'],)).start()
	label=Label(APP,text="From: {0}".format(request.form['name'])) 
	label.pack()
	label=Label(APP,text="E-mail id: {0}".format(request.form['mail'])) 
	label.pack()
	label=Label(APP,text="Phone: {0}".format(request.form['phone'])) 
	label.pack()
	label=Label(APP,text="Message :\n {0}\n----------------------------------------------------".format(request.form['msg'])) 
	label.pack()
	return "YOUR QUERY SUCCESSFULLY SUBMITTED"
@app.route('/dokinter',methods=["POST"])
def flakes2():
	def funcTi(mail):
		fr=open("sender.txt",'r').read()
		password=open('reader.txt','r').read()
		object=SMTP('smtp.gmail.com:587')
		object.starttls()
		object.login(fr,password)
		l=[mail];
		msg={'From':fr,'To':l[0],'Subject':'Do not Reply'}
		mine_mime=MIMEMultipart()
		text=MIMEText('Hello {0} !!!\n Your Query has been successfully submitted\n Thanks For Your Response'.format(l[0]),'plain')
		mine_mime.attach(text)
		for z in msg.keys():
			mine_mime[z]=msg[z]
		msg=mine_mime.as_string()
		object.sendmail(fr,l[0],msg);
		print("Send to"+str(mail))
		object.quit()
	Thread(target=funcTi,args=(request.form['mail'],)).start()
	label=Label(APP,text="From: {0}".format(request.form['name'])) 
	label.pack()
	label=Label(APP,text="E-mail id: {0}".format(request.form['mail'])) 
	label.pack()
	label=Label(APP,text="Message :\n {0}\n----------------------------------------------------".format(request.form['msg'])) 
	label.pack()
	return "YOUR QUERY SUCCESSFULLY SUBMITTED"
@app.route("/slotchange",methods=["POST"])
def flsk():
	data=request.form
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select * from slots ")
	z=pointer.fetchall()
	for i in z:
		if str(i[0]+" "+i[1]) not in request.form.keys():
			pointer.execute("update slots set availability='avail' where department='{0}' and name='{1}'".format(i[0],i[1]))
		else:
			pointer.execute("update slots set availability='filled' where department='{0}' and name='{1}'".format(i[0],i[1]))
	c.commit()
	return "UPDATE SUCCESS"
@app.route('/slotmanage/')
def slotmanage():
	try:
		str(session[request.cookies.get('mail')])
		c=MySQLdb.connect('localhost','labwork','labwork','project')
		pointer=c.cursor()
		pointer.execute("select * from slots")
		z=pointer.fetchall()
		return render_template('slots/slotsmanage.html',mail=request.cookies.get('mail'),data=z)
	except:
		return redirect(url_for('home'))
@app.route('/slotsadd',methods=['POST','GET'])
def slots():
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("insert into slots (name,department,availability) values('{0}','{1}','{2}')".format(request.form['name'],\
	request.form['dept'],request.form['avail']))
	c.commit()
	z=pointer.fetchall()
	return "SLOT ADDED"
@app.route("/dokinter/",methods=['POST'])
def do_kinter():
	Thread(target=my_funct).start()
	return str("SUCCESS")
@app.route('/contact_forum/')
def contact():
	return render_template("contact/index.html")
@app.route('/assignments/')
def assignments():
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select name from files where type='assignment'")
	z=pointer.fetchall()
	return render_template("course/index.html",diction=z)
@app.route('/tutorials/')
def tutorials():
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select name from files where type='tutorial'")
	z=pointer.fetchall()
	return render_template("course/index.html",diction=z)
@app.route('/cse/')
def cse():
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select name from files where department='cse'")
	z=pointer.fetchall()
	return render_template("course/index.html",diction=z)
@app.route('/mnc/')
def mnc():
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select name from files where department='mnc'")
	z=pointer.fetchall()
	return render_template("course/index.html",diction=z)
@app.route('/ee/')
def ee():
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select name from files where department='ee'")
	z=pointer.fetchall()
	return render_template("course/index.html",diction=z)
@app.route('/ece/')
def ece():
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select name from files where department='ece'")
	z=pointer.fetchall()
	return render_template("course/index.html",diction=z)
@app.route('/physics/')
def physics():
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select name from files where department='physics'")
	z=pointer.fetchall()
	return render_template("course/index.html",diction=z)
@app.route('/exampapers/')
def exampapers():
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select name from files where type='exampaper'")
	z=pointer.fetchall()
	return render_template("course/index.html",diction=z)
@app.route('/files/<file>')
def get_file(file):
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	pointer.execute("select file from files where name='{0}'".format(file))
	content=pointer.fetchall()[0][0];
	response=make_response("{0}".format(content))
	response.headers["Content-Disposition"]="attachment;filename={0}".format(file)
	return response;
@app.route('/team/')
def team():
	return render_template("team/index.html")
@app.route('/login_home/')
def home():
	#file=open('data.dat','rb')
	#return str(load(file))
	try:
		req=request.cookies.get('mail')
		if session[req]==request.remote_addr:
			return redirect(url_for('login_success',usr=req))
		else:
			return '<h1>System Security Breach Attempt Failure</h1>'
	except:
		pass
	r=url_for('static',filename='register.jpg')
	u=url_for('static',filename='submit.jpg')
	return render_template("file.html",sub_=u,reg_=r)
@app.route('/login/',methods=["GET","POST"])
def login():
	try:
		data=request.form
		pointer.execute("select K,password from login where name='{0}'".format("".join("".join(data['mail'].split(',')).split(' '))))
		tup=pointer.fetchall()
		#return str(tup)
		if authenticate(tup,data['pswd']):
			session[data['mail']]=request.remote_addr
			session.permanent = True
			app.permanent_session_lifetime = timedelta(days=7)
			cook=make_response(redirect(url_for("login_success",usr=data['mail'])))
			cook.set_cookie('mail',data['mail'],max_age=int(week(1)))
			return cook
	except:
		pass
	return redirect(url_for('log_fail'))
@app.route('/file_upload/' ,methods=['POST'])
def file_upload():
	f=request.files['file']
	c=MySQLdb.connect('localhost','labwork','labwork','project')
	pointer=c.cursor()
	data=f.read()
	name=f.filename
	type=request.form['file_type']
	dep=request.form['dept']
	pointer.execute("insert into files (name,file,type,department) values('{0}','{1}','{2}','{3}')".format(name,data,type,dep))
	c.commit();
	return str("SUCCESS")
@app.route('/log_f/')
def log_fail():
	LOGIN=url_for('static',filename='LOGIN.jpg')
	REG=url_for('static',filename='register.jpg')
	d={ 'msg': 'Invalid Username-Password Combination', 'REG' : REG, 'LOGIN' : LOGIN ,'msg0':'Login Failed'} 
	return render_template("reg_fail.html",**d)
@app.route('/log_suc/<usr>')
def login_success(usr):
	req=request.cookies.get('mail')
	if req!=usr:
		return "404 NOT FOUND  -.-"
	try:
		if session[req]!=request.remote_addr:
			return '<h1>System Security Breach Attempt Failure</h1>'
	except:
		return '<h1>System Security Breach Attempt Failure</h1>'
		pass
	data=get_data(usr)
	return render_template('user_home.html',**data)
@app.route('/logout/',methods=["POST"])
def logout():
	#return str(request.form)
	try:
		session.pop(request.form['mail'],None)
	except:
		pass
	return redirect(url_for('home'))
@app.route('/register/',methods=["GET","POST"])
def register():
	d={'pyth':url_for('static',filename='pyth.jpg'),'res_':url_for('static',filename='reset.jpg'),'sub_':url_for('static',filename='submitbutton.jpg')}
	return render_template("register.html",**d)
@app.route('/reg_success/',methods=['GET','POST'])
def success():
	d=request.form
	try:
		pointer.execute("select exists(select name from login where name ='{0}')".format(d['mail']))
		z=int(pointer.fetchall()[0][0])
		if z:
			return redirect(url_for("registration_failed",msg="User Already exists"))
	except:
		pass
	if d['pswd1']!=d['pswd2']:
		return redirect(url_for("registration_failed",msg="Passwords should be same"))
	K=Fernet.generate_key()
	suite=Fernet(K)
	cipher=suite.encrypt(b"{0}".format(d['pswd1']))
	pointer.execute("insert into login (name,K,password) values('{0}','{1}','{2}')".format(d['mail'],K,cipher))
	pointer.execute("create table {0}(frm varchar(50), too varchar(50),msg varchar(5000),time_stam timestamp)".format(getcharsonly(d['mail'])))
	c.commit()
	def func():
		fr=open("sender.txt",'r').read()
		password=open('reader.txt','r').read()
		object=SMTP('smtp.gmail.com:587')
		object.starttls()
		object.login(fr,password)
		l=[d['mail']];
		msg={'From':fr,'To':l[0],'Subject':'Registration completed'}
		mine_mime=MIMEMultipart()
		text=MIMEText('Hello {0} !!!\n Your account on Course Website is successfully made password :{1}.'.format(l[0],d['pswd1']),'plain')
		mine_mime.attach(text)
		for z in msg.keys():
			mine_mime[z]=msg[z]
		msg=mine_mime.as_string()
		object.sendmail(fr,l[0],msg);
		object.quit()
	Thread(target=func).start()
	return redirect(url_for("registration_successful"))
@app.route('/ref_fail/<msg>',methods=["GET","POST"])
def registration_failed(msg):
		LOGIN=url_for('static',filename='LOGIN.jpg')
		REG=url_for('static',filename='register.jpg')
		d={ 'msg': msg, 'REG' : REG, 'LOGIN' : LOGIN ,'msg0':'Registration Failed'} 
		return render_template("reg_fail.html",**d)
@app.route('/ref_sec/')
def registration_successful():
		SUC=url_for('static',filename='success.jpg')
		LOGIN=url_for('static',filename='LOGIN.jpg')
		d={'LOGIN':LOGIN,'SUCCESS':SUC }
		return render_template("reg_suc.html",**d)
def retrieve(string):
	r=0
	for i in string:
		if i is '@':
			break
		r+=1
	return "".join(string[0:r])
def get_data(usr):
	d={'user':retrieve(usr),'mail':usr,\
		'search':url_for('static',filename='search.jpg'),\
		'sn':url_for('static',filename='s_b.jpg'),'add':url_for('static',filename='add.jpg'),\
		'an':url_for('static',filename='submitbutton.jpg'),\
		'logout':url_for('static',filename='logout.jpg')}
	return d
@app.route('/search/',methods=["GET","POST"])
def srch():
	d=request.form;
	usr=d['mail']
	pointer.execute("select exists(select name from login where name ='{0}')".format(d['search']))
	z=int(pointer.fetchall()[0][0])
	if z:
		log=url_for('static',filename='logout.jpg')
		di={'mail':d['mail'],'user':d['search'],'logout':log}
		di['css']=url_for('static',filename='my_css.css')
		di['sio']=url_for('static',filename='sio.js')
		di['jq']=url_for('static',filename='jquery.js')
		di['my_jsq']=url_for('static',filename='jsq.js')
		return render_template('use2.html',**di)
	return "NO user exists"
@socketio.on('json')
def send(json):
	frm=json['from']
	to=json['to']
	msg=json['msg']
	suite1=Fernet(b'{0}'.format(get_key(frm)))
	suite2=Fernet(b'{0}'.format(get_key(to)))
	msg_from=suite1.encrypt(b"{0}".format(msg))
	msg_to=suite2.encrypt(b"{0}".format(msg))
	date=(str(datetime.now())).split('.')[0]
	pointer.execute("insert into {4}(frm,too,msg,time_stam) values('{0}','{1}','{2}','{3}')".format(frm,to,msg_from,date,getcharsonly(frm)))
	pointer.execute("insert into {4}(frm,too,msg,time_stam) values('{0}','{1}','{2}','{3}')".format(frm,to,msg_to,date,getcharsonly(to)))
	c.commit()
	emit('incoming_text',json,broadcast=True);
def get_key(name):
	pointer.execute("select K from login where name='{0}'".format(name))
	return pointer.fetchall()[0][0]
def msg_sent(message):
	return "Hello world"
def min(x):
	return 60*x
def hour(x):
	return min(x*60)
def day(x):
	return hour(24*x)
def week(x):
	return day(7*x)
def month(x):
	return day(30*x)
def year(x):
	return day(365*x)
def my_funct():
	label=Label(text=0,font=('Monotype corsiva',20),width=30)
	label.pack()
def authenticate(tup,pswd):
	if not len(tup):
		return False
	suite=Fernet(b'{0}'.format(tup[0][0]))
	if suite.decrypt(b'{0}'.format(tup[0][1]))==pswd:
		return True
	else:
		return False
def getcharsonly(S):
	z=""
	for i in S:
		if i not in ('@','.'):
			z+=i
	return z
#KINTER 
def my_function():
	'''global tkin
	tkin=Tk()
	tkin.geometry("500x600")
	tkin.mainloop()'''
	return 4;
if __name__ == '__main__':
	Thread(target=my_function).start()
	socketio.run(app,port=9001,host='0.0.0.0',debug=True)
	