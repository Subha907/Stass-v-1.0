from flask import Flask,render_template,request,flash,redirect,make_response,session
from flask_mail import Mail,Message
#import bcrypt
import pdfkit
#import os
import mysql.connector
#import wkhtmltopdf
app=Flask(__name__)
#mail=Mail(app)
#WKHTMLTOPDF_BIN_PATH = r'F:\wkhtmltopdf'
#PDF_DIR_PATH =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'pdf')
#WKHTMLTOPDF_USE_CELERY = True
#wkhtmltopdf = Wkhtmltopdf(app)
config = {
  'user': 'Stass',
  'password': '1999*Subh@',
  'host': 'Stass.mysql.pythonanywhere-services.com',
  'database': 'Stass$stasstest'
}
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'stassbooking@gmail.com'
app.config['MAIL_PASSWORD'] = 'dbfpwaqwwjiauout'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail=Mail(app)
PDFKIT_CONFIGURATION = pdfkit.configuration(wkhtmltopdf='/home/Stass/wkhtml-install/usr/local/bin/wkhtmltopdf')
app.secret_key = 'many random bytes'
#mycursor=mydb.cursor()

@app.route('/',methods=['POST','GET'])
def index():
        return render_template('cool1.html')
@app.route('/sususataan',methods=['POST','GET'])
def signup():
        if request.method =='POST':
            signup=request.form
            print(signup)
            name=signup['Username']
            birthdate=signup['Password']
            #mycursor.execute("insert into dob(name,birthdate) values(%s,%s)",(name,birthdate))
            #mydb.commit()
            #mycursor.close()
            if not len(birthdate)>=5:
                flash("password must be atleast 5 characters","warning")
                return redirect('/sususataan')
            else:
                #hashed=bcrypt.hashpw(birthdate.enconde('utf-8'),bcrypt.gensalt())
                #mycursor.execute("insert into dob(name,birthdate,hash) values(%s,%s,%s)",(name,birthdate,hashed))
                mydb=mysql.connector.connect(**config)
                mycursor=mydb.cursor()
                mycursor.execute("insert into dob(name,birthdate) values(%s,%s)",(name,birthdate))
                mydb.commit()
                mycursor.close()
                mydb.close()
                flash("Registered successfully ,Please login again to go to dashboard","success")
                return redirect('/login')

        return render_template('signup.html')
#app.run(debug=True)
@app.route('/login')
def login():
  return render_template('login1.html')
@app.route('/dashboard$',methods=['POST','GET'])
def dashboard():
        if request.method=='POST':
          session['username']=request.form['Username']
          #username=request.form['Username']
          session['passw']=request.form['Password']
          #passw=request.form['Password']
          #print(session['username'])
          mydb=mysql.connector.connect(**config)
          mycursor=mydb.cursor()
          sql="SELECT * FROM dob WHERE name= %s AND birthdate= %s"
          #params=(username,passw)
          params=(session['username'],session['passw'])
          mycursor.execute(sql,params)
          val=mycursor.fetchall()
          mycursor.close()
          mydb.close()
          if(len(val)!=0):
            msg=session['username']
            return render_template('dashboard.html',name=msg)
          else:
            flash("Wrong password","danger")
            return redirect('/login')

@app.route('/dashboard')
def dashboard1():
    if 'username' in session:
        msg=session['username']
        return render_template('dashboard1.html',name=msg)
    else:
        flash("Please Login To Access Dashboard","warning")
        return redirect('/login')
    return render_template('dashboard1.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully","success")
    return redirect('/login')

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

##for doctor database#########

@app.route('/dcheck')
def dcheck():
    #mycursor.execute("SELECT * FROM doctor")
    #data=mycursor.fetchall()
    #mycursor.execute("SELECT * FROM patient")
    #data1=mycursor.fetchall()
    #return render_template('check.html',data=data,data1=data1)
    if 'username' in session:
        #msg=session['username']
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        mycursor.execute("SELECT * from doctor")
        data=mycursor.fetchall()
        #mycursor.execute("SELECT * FROM patient")
        #data1=mycursor.fetchall()
        print(data)
        if(len(data)==0):
          flash("No entries yet","no-entries")
          return render_template('dcheck.html')
        '''if(len(data1)==0):
          flash("No entries yet","no-entries-pa")
          return render_template('dcheck.html')'''
        if(len(data)!=0):
          return render_template('dcheck.html',data=data)
        '''if(len(data1)!=0):
          return render_template('check.html',data1=data1)'''
        mycursor.close()
        mydb.close()
    else:
        flash("Please Login To Access Dashboard","warning")
        return redirect('/login')
@app.route('/newEntry', methods=['POST','GET'])
def newEntry():
  if(request.method =='POST'):
    data=request.form
    dname=data['dname']
    specialization=data['specialization']
    PhoneNo=data['PhoneNo']
    Email=data['Email']
    DOB=data['DOB']
    Days=data['Days']
    Time=data['Time']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    mycursor.execute("insert into doctor(Doname,phoneno,email,specialization,DOB,Days,Time) values(%s,%s,%s,%s,%s,%s,%s)",(dname,PhoneNo,Email,specialization,DOB,Days,Time))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return redirect('/dcheck')
@app.route("/ddelete/<string:id>",methods=['GET','POST'])
def ddelete(id):
  #data=request.form
  #ID=data['ID']
  #print(data)
  mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  #mycursor.execute("delete from Doctor where id=%s",(id));
  mycursor.execute("""DELETE FROM doctor WHERE id LIKE '{}'""".format(id))
  mydb.commit()
  mycursor.close()
  mydb.close()
  return redirect('/dcheck')

@app.route("/dupdate/<string:id>",methods=['GET','POST'])
def dupdate(id):
  mydb=mysql.connector.connect(**config)
  if(request.method =='POST'):
    data=request.form
    dname=data['dname']
    specialization=data['specialization']
    PhoneNo=data['PhoneNo']
    Email=data['Email']
    DOB=data['DOB']
    Days=data['Days']
    Time=data['Time']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    sql="update doctor set Doname=%s,specialization=%s,phoneno=%s,email=%s,DOB=%s,Days=%s,Time=%s where id=%s"
    #mycursor.execute("insert into Doctor(dname,specialization,PhoneNo,Email,DOB) values(%s,%s,%s,%s,%s)",(dname,specialization,PhoneNo,Email,DOB))
    #mycursor.execute("""UPDATE Doctor SET dname LIKE '{}',specialization LIKE '{}',PhoneNo LIKE '{}',Email LIKE '{}',DOB LIKE '{}'""".format(dname,specialization,PhoneNo,Email,DOB))
    mycursor.execute(sql,[dname,specialization,PhoneNo,Email,DOB,Days,Time,id])
    mydb.commit()
    mycursor.close()
    mydb.close()
    flash("entries updated","entries-mssg")
    return redirect('/dcheck')
  #mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  #mycursor.execute("""SELECT * Doctor WHERE id LIKE '{}'""".format(id))
  sql="select * from doctor where id=%s"
  mycursor.execute(sql,[id])
  datas=mycursor.fetchall()
  print(datas)
  mycursor.close()
  mydb.close()
  return render_template('dupdate.html',datas=datas)

#### For Patient database  ####

@app.route('/pcheck')
def pcheck():
    if 'username' in session:
        mydb=mysql.connector.connect(**config)
        mycursor=mydb.cursor()
        mycursor.execute("SELECT * FROM patient")
        data1=mycursor.fetchall()
        print(data1)
        if(len(data1)==0):
          flash("No entries yet","no-entries-pa")
          return render_template('pcheck.html')
        if(len(data1)!=0):
          return render_template('pcheck.html',data1=data1)
        mycursor.close()
        mydb.close()
    else:
        flash("Please Login To Access Dashboard","warning")
        return redirect('/login')

@app.route('/pnewEntry', methods=['POST','GET'])
def pnewEntry():
  if(request.method =='POST'):
    data=request.form
    dname=data['dname']
    specialization=data['specialization']
    pname=data['pname']
    pmobileno=data['pmobileno']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    mycursor.execute("insert into patient(Doname,specialization,patientN,patientM) values(%s,%s,%s,%s)",(dname,specialization,pname,pmobileno))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return redirect('/pcheck')

@app.route("/pdelete/<string:id>",methods=['GET','POST'])
def pdelete(id):
  #data=request.form
  #ID=data['ID']
  #print(data)
  mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  mycursor.execute("""DELETE FROM patient WHERE id LIKE '{}'""".format(id))
  mydb.commit()
  mycursor.close()
  mydb.close()
  return redirect('/pcheck')

@app.route("/pupdate/<string:id>",methods=['GET','POST'])
def pupdate(id):
  mydb=mysql.connector.connect(**config)
  if(request.method =='POST'):
    data=request.form
    dname=data['dname']
    specialization=data['specialization']
    pname=data['pname']
    pmobileno=data['pmobileno']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    sql="update patient set Doname=%s,specialization=%s,patientN=%s,patientM=%s where id=%s"
    #mycursor.execute("insert into Doctor(dname,specialization,PhoneNo,Email,DOB) values(%s,%s,%s,%s,%s)",(dname,specialization,PhoneNo,Email,DOB))
    #mycursor.execute("""UPDATE Doctor SET dname LIKE '{}',specialization LIKE '{}',PhoneNo LIKE '{}',Email LIKE '{}',DOB LIKE '{}'""".format(dname,specialization,PhoneNo,Email,DOB))
    mycursor.execute(sql,[dname,specialization,pname,pmobileno,id])
    mydb.commit()
    mycursor.close()
    mydb.close()
    flash("entries updated","entries-mssg")
    return redirect('/pcheck')
  #mydb=mysql.connector.connect(**config)
  mycursor=mydb.cursor()
  #mycursor.execute("""SELECT * Doctor WHERE id LIKE '{}'""".format(id))
  sql="select * from patient where id=%s"
  mycursor.execute(sql,[id])
  datas=mycursor.fetchall()
  print(datas)
  mycursor.close()
  mydb.close()
  return render_template('pupdate.html',datas=datas)

@app.route('/booking')
def booking():
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    mycursor.execute("SELECT id,Doname FROM doctor")
    doctor=mycursor.fetchall()
    mycursor.execute("SELECT id,specialization FROM doctor")
    specialization=mycursor.fetchall()
    mycursor.close()
    mydb.close()
    print(doctor)
    if (len(doctor)>0) and (len(specialization)>0):
            return render_template('book.html',doctor=doctor,specialization=specialization)


@app.route('/bookingProcessing',methods=['POST','GET'])
def bookingProcessing():
        t=0
        if request.method =='POST':
            book=request.form
            doctor=book['doctor']
            specialization=book['specialization']
            patientN=book['patientN']
            patientM=book['patientM']
            if len(doctor)== 0:
                flash("Please select a doctor from the drop down","warning")
                return redirect('/booking')
            if len(specialization)== 0:
                flash("Please select a specialization from the drop down","warning")
                return redirect('/booking')
            if len(patientN)== 0:
                flash("please enter the name","warning")
                return redirect('/booking')
            if len(patientM)!= 10:
                flash("please enter a valid phone number","warning")
                return redirect('/booking')
            mydb=mysql.connector.connect(**config)
            mycursor=mydb.cursor()
            mycursor.execute("insert into patient(Doname,specialization,patientN,patientM) values(%s,%s,%s,%s)",(doctor,specialization,patientN,patientM))
            mydb.commit()
            #flash("booking Confirmed","success")
            #mycursor.execute("SELECT id,Doname,specialization,patientN,patientM FROM WHERE patientN = %s and patientM = %s",)
            mycursor.execute("""SELECT id,Doname,specialization,patientN,patientM FROM patient WHERE patientN LIKE '{}' AND patientM LIKE '{}'""".format(patientN,patientM))
            patient=mycursor.fetchall()
            mycursor.close()
            mydb.close()
            #print(patient)
            Id=patient[0][0]
            #print(Id)
            Doname=patient[0][1]
            #print(Doname)
            specialization=patient[0][2]
            #print(specialization)
            patientN=patient[0][3]
            #print(patientN)
            patientM=patient[0][4]
            #print(patientM)
            html=render_template('pdfGenerate2.html',Id=Id,Doname=Doname,specialization=specialization,patientN=patientN,patientM=patientM)
            pdf=pdfkit.from_string(html, False,configuration=PDFKIT_CONFIGURATION)
            response=make_response(pdf)
            response.headers["Content-Type"]="application/pdf"
            response.headers["Content-Disposition"]="inline; filename=output.pdf"
            return response
@app.route('/delete',methods=['POST','GET'])
def delete():
    if request.method=='POST':
        fetch=request.form
        print(fetch)
        delete1=fetch['delete']
        print(delete1)
        if(len(delete1)==0):
            flash("delete section is empty","warning")
            return render_template('pcheck.html')
        if(delete1!=1):
            flash("please type 1 to delete","warning")
            return render_template('pcheck.html')
        if(len(delete1)==1):
            mycursor.execute("DELETE FROM patient")
            mydb.commit()
            flash("Records deleted successfully","success")
            return render_template('pcheck.html')
'''@app.route('/dregistration',methods=['POST','GET'])
def dregistration():
    if request.method=='POST':
        dregistration=request.form
        print(dregistration)
        NAME=dregistration['NAME']
        SPECIALIZATION=dregistration['SPECIALIZATION']
        PHONENO=dregistration['PHONE NO']
        EMAILID=dregistration['EMAIL ID']
        DOB=dregistration['DOB']
        if(len(NAME)==0 and len(SPECIALIZATION)==0 and len(PHONENO)==0 and len(EMAILID)==0 and len(DOB)==0):
            flash("please fill up the fields","warning")
            return redirect('/dregistration')
        mycursor.execute("insert into doctor(Doname,phoneno,email,specialization,DOB) values(%s,%s,%s,%s,%s)",(NAME,PHONENO,EMAILID,SPECIALIZATION,DOB))
        mydb.commit()
        flash("Registered successfully","success")
        return redirect('/dregistration')
    return render_template('registration.html')'''
@app.route('/contacts')
def contacts():
  return render_template('contacts2.html')
@app.route("/inform", methods=['POST', 'GET'])
def inform():
    if request.method == "POST":
        name = request.form["name"]
        email =request.form["email"]
        number=request.form["number"]
        message = request.form["message"]
        print(name)
    #msg = Message(sub, sender='stassbooking@gmail.com', recipients=['sayantan.bose286@gmail.com'])
    #msg.body = maill
    mail.send_message('Notification From Client',sender='stassbooking@gmail.com',recipients=['stassbooking@gmail.com'],body=message+"\n" + name+ "\n" + "Email : "+ email +"\n" + "Phone No.:"+ number)
    mail.send_message('Notification',sender='stassbooking@gmail.com',recipients=[email],body="We will contact you soon!"+"\n"+"Regards From"+"\n"+"STASS TEAM")
    #return "<h1>Thanks For Contacting Us!<h1><h2>We will Communicate You Soon<h2>"
    return render_template('thanks32.html')

@app.route('/about')
def about():
  return render_template('about2.html')

@app.route('/doctor-Chart-PDF')
def chart():
    #mycursor.execute("SELECT * FROM doctor")
    #data=mycursor.fetchall()
    #mycursor.execute("SELECT * FROM patient")
    #data1=mycursor.fetchall()
    #return render_template('check.html',data=data,data1=data1)
    ##msg=session['username']
    mydb=mysql.connector.connect(**config)
    mycursor=mydb.cursor()
    mycursor.execute("SELECT Doname,specialization,Days,Time from doctor")
    data=mycursor.fetchall()
    #mycursor.execute("SELECT * FROM patient")
    #data1=mycursor.fetchall()
    print(data)
    if(len(data)==0):
      flash("No entries yet","no-entries")
      return render_template('dcheck.html')
    if(len(data)!=0):
      html=render_template('doctor.html',data=data)
      pdf=pdfkit.from_string(html, False,configuration=PDFKIT_CONFIGURATION)
      response=make_response(pdf)
      response.headers["Content-Type"]="application/pdf"
      response.headers["Content-Disposition"]="inline; filename=DoctorChart.pdf"
      return response
    mycursor.close()
    mydb.close()

if __name__ == '__main__':
   app.run(debug=False,host='0.0.0.0')

