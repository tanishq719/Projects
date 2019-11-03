import os
from flask import Flask, render_template, request, session, jsonify, json, redirect, flash
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from models.tables import *
from functools import wraps
import pickle

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tanishq719@localhost/event'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_PERMANENT'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.urandom(24)
db.init_app(app)

bcrypt = Bcrypt(app)

def check_login(f):
    @wraps(f)
    def isLoggedIn():
        if 'loggedIn' in session :
            return f(True)
        else:
            return f(False)
    return isLoggedIn

@app.route('/')
@check_login
def index(loggedIn):
    db.create_all()
    if loggedIn:
        # print(session['User'])
        o1 = session.get('User')
        u1 = pickle.loads(o1)
        return render_template('index.html', loggedIn = loggedIn, name = u1.getFName() + " "+ u1.getLName(), options = u1.getDropDown())

    return render_template('index.html', loggedIn = loggedIn)


@app.route('/signup', methods=["GET", "POST"])
@check_login
def signup(loggedIn):
    if loggedIn:
        # return redirect(request.referrer)
        return render_template('error.html', alert="already logged in, logout first")
    stateList = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
    list1 = ['Cattring', 'Stage Decorater', 'Electricity', 'Water Supplier']
    if(request.method == 'POST'):

        # variable formation :
        email = request.form.get("email")
        password = request.form.get("password")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        phone = request.form.get("phone")
        acceptTermsNCond = request.form.getlist("check")
        userType = request.form.get("options")
        adderess = request.form.get("adderess")
        description = request.form.get("descript")
        city = request.form.get("city")
        state = request.form.get("state")
        zzip = request.form.get("zip")
        website = request.form.get("website")
        service_selected = request.form.get("services")

        # some checks on the form :
        if(len(acceptTermsNCond) == 0):     # getlist will form list in anyway, there in case of not selecting its length will be 0
            return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList, error=True, alert="terms and conditions are not accepted")
    
        duplicatAtt = Event_Attender.query.filter_by(
                ea_email=email).first()
        
        if(duplicatAtt is not None):
            return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList,error=True, alert="user with the same email id already exist")

        if(userType == '-1'):
            return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList,error=True, alert="who i am not selected")
        
        # based on selected user type data is feeded here:
        elif(userType == '1'):
        
            if((email == "") or (password == "") or (firstName == "") or (lastName == "")):
                return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList,error=True, alert="fields having * are mandatory ")
            
            attender = Event_Attender(
                ea_email = email, first_name = firstName, last_name = lastName, password = password, ph_no = phone)
            db.session.add(attender)
       
            u1 = pickle.dumps(attender)
            session['User'] = u1
            session['UserType'] = 'EVENT_ATTENDER'
            session['loggedIn'] = 'YES'
            db.session.commit()
            return redirect('/')
            
                
        elif(userType == '2'):
            if((email == "") or (password == "") or (firstName == "") or (lastName == "") or (adderess == "") or (state == "") or (city == "") or (zzip == "")):
                return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList,error=True, alert="fields having * are mandatory ")

            add = adderess.split(",")

            if(len(add) == 3):
                add_id = add[0].strip() + add[1].strip()+add[2].strip()+ zzip
            elif(len(add) == 1):
                return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList,error=True, alert="in adderess no and street name are compulsary")
            elif(add[1].isdigit()):
                return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList,error=True, alert="in adderess no and street name are compulsary")
            else:
                add_id = add[0].strip() + add[1].strip()+ zzip

            pre_add_id = Adderess.query.filter_by(adderess_id = add_id).first()
            if(pre_add_id == None):
                if(len(add)==3):
                    Cladderess = Adderess(adderess_id = add_id, no = int(add[0].strip()), street_name = add[1].strip(), apt_no = int(add[2].strip()), description = description, city = city, state = stateList[int(state)-1], zipcode = int(zzip))
                else:
                    Cladderess = Adderess(adderess_id = add_id, no = int(add[0].strip()), street_name = add[1].strip(), description = description, city = city, state = stateList[int(state)-1], zipcode = int(zzip))
                db.session.add(Cladderess)
                db.session.commit()

            client = Client(c_email_id = email, first_name = firstName, last_name = lastName, password = password, ph_no = phone, adderess_id = add_id)

            db.session.add(client)
            u1 = pickle.dumps(client)
            session['User'] = u1
            session['UserType'] = 'CLIENT'
            session['loggedIn'] = 'YES'
            db.session.commit()
            return redirect('/')

        elif(userType == '3'):
            if((email == "") or (password == "") or (firstName == "") or (lastName == "") or (adderess == "") or (state == "") or (city == "") or (zzip == "") or (website == "")):
                return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList,error=True, alert="fields having * are mandatory ")

            add = adderess.split(",")

            if(len(add) == 3):
                add_id = add[0].strip() + add[1].strip()+add[2].strip()+ zzip
            elif(len(add) == 1):
                return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList,error=True, alert="in adderess no and street name are compulsary")
            elif(add[1].isdigit()):
                return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList,error=True, alert="in adderess no and street name are compulsary")
            else:
                add_id = add[0].strip() + add[1].strip()+ zzip

            pre_add_id = Adderess.query.filter_by(adderess_id = add_id).first()
            if(pre_add_id == None):
                if(len(add)==3):
                    Cladderess = Adderess(adderess_id = add_id, no = int(add[0].strip()), street_name = add[1].strip(), apt_no = int(add[2].strip()), description = description, city = city, state = stateList[int(state)-1], zipcode = int(zzip))
                else:
                    Cladderess = Adderess(adderess_id = add_id, no = int(add[0].strip()), street_name = add[1].strip(), description = description, city = city, state = stateList[int(state)-1], zipcode = int(zzip))
                db.session.add(Cladderess)
                db.session.commit()

            sponser = Sponser(semail_id = email, s_fname = firstName, s_lname = lastName, password = password, ph_no = phone, website = website, adderess_id = add_id)

            u1 = pickle.dumps(sponser)
            session['User'] = u1
            session['UserType'] = 'Sponser'
            session['loggedIn'] = 'YES'
            db.session.commit()
            return redirect('/')

        elif(userType == '4'):

            if((email == "") or (password == "") or (firstName == "") or (lastName == "") or (adderess == "") or (state == "") or (city == "") or (zzip == "") or (website == "") or (service_selected == "")):
                return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList=stateList, error=True, alert="fields having * are mandatory")

            add = adderess.split(",")

            if(len(add) == 3):
                add_id = add[0].strip() + add[1].strip()+add[2].strip()+ zzip
            elif(len(add) == 1):
                return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList,error=True, alert="in adderess no and street name are compulsary")
            elif(add[1].isdigit()):
                return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList,error=True, alert="in adderess no and street name are compulsary")
            else:
                add_id = add[0].strip() + add[1].strip()+ zzip
                
            pre_add_id = Adderess.query.filter_by(adderess_id = add_id).first()
            if(pre_add_id == None):
                if(len(add)==3):
                    Cladderess = Adderess(adderess_id = add_id, no = int(add[0].strip()), street_name = add[1].strip(), apt_no = int(add[2].strip()), description = description, city = city, state = stateList[int(state)-1], zipcode = int(zzip))
                else:
                    Cladderess = Adderess(adderess_id = add_id, no = int(add[0].strip()), street_name = add[1].strip(), description = description, city = city, state = stateList[int(state)-1], zipcode = int(zzip))
                db.session.add(Cladderess)
                db.session.commit()

            serv_id = Services.query.filter_by(service_name = list1[int(service_selected) - 1]).first()
            if(serv_id == None):
                service = Services(service_name = list1[int(service_selected) - 1])
                db.session.add(service)
                db.session.commit()
                serv_id = Services.query.filter_by(service_name = list1[int(service_selected) - 1]).first()

            print(type(serv_id))
            service_pro = Service_Provider(sp_email_id = email, sp_fname = firstName, sp_lname = lastName, password = password, ph_no = phone, website = website, adderess_id = add_id, ser_id = serv_id.ser_id)

            u1 = pickle.dumps(service_pro)
            session['User'] = u1
            session['UserType'] = 'SERVICE_PROVIDER'
            session['loggedIn'] = 'YES'
            db.session.commit()
            return redirect('/')
        
    return render_template('signup.html', loggedIn=False, servicesOffered=list1, stateList = stateList, error=False, alert="")


@app.route('/login', methods= ['GET','POST'])
@check_login
def login(loggedIn):
    
    if loggedIn:
        # return redirect(request.referrer)
        return render_template('error.html', alert="already logged in")

    if(request.method == "POST"):
        email = request.form.get("email")
        password = request.form.get("password") 
        users = [Event_Attender, Sponser, Service_Provider, Client, Company_Employee]
       
        for i in range(5):
            output, user = users[i].check_credentials(email,password)
            print(users[i].__name__)
            if output == 'PWSMATCHED':
                u1 = pickle.dumps(user)
                session['User'] = u1
                session['UserType'] = users[i].__name__.upper()
                session['loggedIn'] = 'YES'
                return redirect('/')
            
            elif output == 'PWSNOTMATCHED':
                flash("password doesnt matches with the email")
                break
            else:
                flash("Invalid email")
                break

        return render_template('login.html', loggedIn=loggedIn)
        
    return render_template('login.html', loggedIn=loggedIn)

@app.route('/logout')
@check_login
def logout(loggedIn):
    if not loggedIn:
        return render_template('error.html', alert="You are already logged out")
    else:
        session.pop('User', None)
        session.pop('UserType',None)
        session.pop('loggedIn', None)
        return render_template('index.html', loggedIn = not(loggedIn))


@app.route('/profile')
@check_login
def profile(loggedIn):
    return render_template('profile.html', loggedIn = loggedIn)

@app.route('/history')
@check_login
def history(loggedIn):
    return render_template('history.html', loggedIn = loggedIn)

@app.route('/notification')
@check_login
def notification(loggedIn):
    return render_template('notification.html', loggedIn = loggedIn)

@app.route('/feedback')
@check_login
def feedback(loggedIn):
    return render_template('feedback.html', loggedIn = loggedIn)

@app.route('/termsncond')
def termsncond():
    return render_template('termsncond.html')


if __name__ == "__main__":
    app.run(debug=True)
