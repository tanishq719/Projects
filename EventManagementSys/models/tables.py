from flask_sqlalchemy import SQLAlchemy
from abc import ABC, abstractmethod
db = SQLAlchemy()

# attends1 = db.Table(
# 	'attends',
# 	db.Column('ea_email', db.VARCHAR(length = 20), db.ForeignKey('event_attender.ea_email'), primary_key = True),
# 	db.Column('e_sdate', db.TIMESTAMP, primary_key = True),
# 	db.Column('location_id',db.VARCHAR(length = 10), primary_key=True),
# 	db.Column('dateofregistration',db.TIMESTAMP, nullable = False),
# 	db.Column('ticket',db.JSON, nullable = False),

# 	__table_args__ = (
# 						db.ForeignKeyConstraint(
# 							['e_sdate', 'location_id'],
# 							['Event1.e_sdate', 'Event1.location_id']

# 						,),
# 					)
# )

class Event_Attender(db.Model):
	__tablename__ = 'event_attender'
	ea_email = db.Column(db.VARCHAR(length = 50), primary_key = True)
	first_name = db.Column(db.VARCHAR(length = 30), nullable = False)
	last_name = db.Column(db.VARCHAR(length = 30), nullable = False)
	password = db.Column(db.VARCHAR(length = 65), nullable = False)
	ph_no = db.Column(db.VARCHAR(length = 12))
	event = db.relationship('Event1', secondary = 'attends', cascade = 'all, delete', backref = db.backref('attended_by', lazy = True))
	company_center = db.relationship('Company_Center', secondary = 'comunicatecc', cascade = 'all, delete', backref = db.backref('have_attender', lazy=True))

	@staticmethod
	def check_credentials(email, password):
		Uoutput = Event_Attender.query.filter_by(ea_email = email).first()
		if Uoutput == None:
			return None, None
		elif Uoutput.password != password :
			return 'PWSNOTMATCHED', None
		else:
			return 'PWSMATCHED', Uoutput

	@staticmethod
	def getDropDown():
		d = {'Profile':"profile", 'History':"history",
			'Notification':'notification', 'Feedback':'feedback',
			'Logout':'logout'}
		return d

	def getEmail(self):
		return self.ea_email

	def getFName(self):
		return self.first_name

	def getLName(self):
		return self.last_name

	def getPassword(self):
		return self.password

	def getPhone(self):
		return self.ph_no

	def setEmail(self, email):
		self.ea_email = email
		db.session.commit()

	def setFName(self,fname):
		self.first_name = fname
		db.session.commit()

	def setLName(self, lname):
		self.last_name = lname
		db.session.commit()

	def setPassword(self, password):
		self.password = password
		db.session.commit()

	def setPhone(self, phone):
		self.ph_no = phone
		db.session.commit()

class Adderess(db.Model):
	__tablename__ = 'adderess'
	adderess_id = db.Column(db.VARCHAR(130), primary_key = True)
	no = db.Column(db.Integer)
	street_name = db.Column(db.VARCHAR(100))
	apt_no = db.Column(db.Integer)
	zipcode = db.Column(db.Integer, nullable = False)
	description = db.Column(db.VARCHAR(150))
	city = db.Column(db.VARCHAR(50), nullable = False)
	state = db.Column(db.VARCHAR(50), nullable = False)
	client = db.relationship('Client', backref = 'adderess', uselist = False)
	company_employee = db.relationship('Company_Employee', backref = 'adderess', uselist = False)
	company_center = db.relationship('Company_Center', backref = 'adderess', uselist = False)
	service_provider = db.relationship('Service_Provider', backref = 'adderess', uselist = False)	
	location  = db.relationship('Location', cascade = 'all, delete', backref = db.backref('adderess', lazy=True), uselist = False)
	sponser = db.relationship('Sponser', cascade = 'all, delete', backref = db.backref('adderess', lazy=True), uselist = False)



class Client(db.Model):
	__tablename__ = 'client'
	c_email_id = db.Column(db.VARCHAR(50), primary_key = True)
	first_name = db.Column(db.VARCHAR(length = 30), nullable = False)
	last_name = db.Column(db.VARCHAR(length = 30), nullable = False)
	password = db.Column(db.VARCHAR(length = 65), nullable = False)
	ph_no = db.Column(db.VARCHAR(length = 12))
	adderess_id = db.Column(db.VARCHAR(length = 130), db.ForeignKey('adderess.adderess_id'), nullable = False)
	company_center = db.relationship('Company_Center', secondary = 'comunicatec', cascade = 'all, delete', backref = db.backref('have_client', lazy=True))

	@staticmethod
	def check_credentials(email, password):
		Uoutput = Client.query.filter_by(c_email_id = email).first()
		if Uoutput == None:
			return None, None
		elif Uoutput.password != password :
			return 'PWSNOTMATCHED', None
		else:
			return 'PWSMATCHED', Uoutput

	@staticmethod
	def getDropDown():
		d = {'Profile':"profile", 'History':"history",
			'Notification':"notification", 'Feedback':"feedback",
			'Logout':"logout"}
		return d

	def getEmail(self):
		return self.c_email_id

	def getFName(self):
		return self.first_name

	def getLName(self):
		return self.last_name

	def getPassword(self):
		return self.password

	def getPhone(self):
		return self.ph_no

	def setEmail(self, email):
		self.c_email_id = email
		db.session.commit()

	def setFName(self,fname):
		self.first_name = fname
		db.session.commit()

	def setLName(self, lname):
		self.last_name = lname
		db.session.commit()

	def setPassword(self, password):
		self.password = password
		db.session.commit()

	def setPhone(self, phone):
		self.ph_no = phone
		db.session.commit()

class Company_Employee(db.Model):
	__tablename__ = 'company_employee'
	ssn = db.Column(db.VARCHAR(20), primary_key = True)
	first_name = db.Column(db.VARCHAR(length = 30), nullable = False)
	last_name = db.Column(db.VARCHAR(length = 30), nullable = False)
	designation = db.Column(db.VARCHAR(length = 100), nullable = False)
	cc_email_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey('company_center.cc_email_id'))
	sdate_time = db.Column(db.TIMESTAMP)
	email = db.Column(db.VARCHAR(length = 50), nullable = False)
	password = db.Column(db.VARCHAR(length = 65), nullable = False)
	ph_no = db.Column(db.VARCHAR(length = 12))
	adderess_id = db.Column(db.VARCHAR(length = 130), db.ForeignKey('adderess.adderess_id'), nullable = False)	# dont know how to impliment on delete set null
	
	@staticmethod
	def check_credentials(email, password):
		Uoutput = Company_Employee.query.filter_by(email = email).first()
		if Uoutput == None:
			return None, None
		elif Uoutput.password != password :
			return 'PWSNOTMATCHED', None
		else:
			return 'PWSMATCHED', Uoutput

	@staticmethod
	def getDropDown():
		d = {'Profile':"profile", 'History':"history",
			'Notification':"notification", 'Feedback':"feedback",
			'Logout':"logout"}
		return d

	def getSsn(self):
		return self.ssn

	def getDesignation(self):
		return self.designation

	def getSDateTime(self):
		return self.sdate_time

	def getEmail(self):
		return self.email

	def getFName(self):
		return self.first_name

	def getLName(self):
		return self.last_name

	def getPassword(self):
		return self.password

	def getPhone(self):
		return self.ph_no

	def setSsn(self, ssn):
		self.ssn = ssn
		db.session.commit()

	def setDesignation(self, designation):
		self.designation = designation
		db.session.commit()

	def setSDateTime(self, sdate_time):
		self.sdate_time = sdate_time
		db.session.commit()

	def setEmail(self, email):
		self.email = email
		db.session.commit()

	def setFName(self,fname):
		self.first_name = fname
		db.session.commit()

	def setLName(self, lname):
		self.last_name = lname
		db.session.commit()

	def setPassword(self, password):
		self.password = password
		db.session.commit()

	def setPhone(self, phone):
		self.ph_no = phone
		db.session.commit()

class Company_Center(db.Model):
	__tablename__ = 'company_center'
	cc_email_id = db.Column(db.VARCHAR(length = 50), primary_key = True)
	# manager_id = db.Column(db.VARCHAR(length = 20), db.ForeignKey('company_employee.ssn'))
	# eplanar_id = db.Column(db.VARCHAR(length = 20), db.ForeignKey('company_employee.ssn'))
	# ticketsalesmg_id = db.Column(db.VARCHAR(length = 20), db.ForeignKey('company_employee.ssn'))
	ph_no = db.Column(db.VARCHAR(length = 12))
	adderess_id = db.Column(db.VARCHAR(length = 130), db.ForeignKey('adderess.adderess_id'), nullable = False)	
	event1 = db.relationship('Event1', cascade = 'all, delete', backref =db.backref('company_center', lazy=True))
	belonged_by = db.relationship('Company_Employee', cascade = 'all, delete', backref = db.backref('company_center', lazy = True))
	prev_belonged_by = db.relationship('Old_CompanyDatabase', cascade = 'all, delete', backref = db.backref('company_center', lazy = True))

class Services(db.Model):
	__tablename__ = 'services'
	ser_id = db.Column(db.Integer, primary_key = True)
	service_name = db.Column(db.VARCHAR(length = 100))
	service_provider = db.relationship('Service_Provider', cascade = 'all, delete', backref = db.backref('services', lazy=True))	# uselist is not set to false because relationship here is one to many

# 	Grand openings
# Client Engagement
# Branding and product launch
# Annual meetings
# Press conferences
# Sales meeting.

class Service_Provider(db.Model):
	__tablename__ = 'service_provider'
	sp_email_id = db.Column(db.VARCHAR(length = 50), primary_key = True)
	sp_fname = db.Column(db.VARCHAR(length = 30), nullable = False)
	sp_lname = db.Column(db.VARCHAR(length = 30), nullable = False)
	password = db.Column(db.VARCHAR(length = 65), nullable = False)
	ser_id = db.Column(db.Integer, db.ForeignKey('services.ser_id'), nullable = False)
	ph_no = db.Column(db.VARCHAR(length = 12))
	website = db.Column(db.VARCHAR(length = 50))
	adderess_id = db.Column(db.VARCHAR(length = 130), db.ForeignKey('adderess.adderess_id'), nullable = False)
	event = db.relationship('Event1', secondary = 'works_for', cascade = 'all, delete', backref = db.backref('have_service_provider', lazy=True))

	@staticmethod
	def check_credentials(email, password):
		Uoutput = Service_Provider.query.filter_by(sp_email_id = email).first()
		if Uoutput == None:
			return None, None
		elif Uoutput.password != password :
			return 'PWSNOTMATCHED', None
		else:
			return 'PWSMATCHED', Uoutput

	@staticmethod
	def getDropDown():
		d = {'Profile':"profile", 'History':"history",
			'Notification':"notification", 'Feedback':"feedback",
			'Logout':"logout"}
		return d

	def getWebsite(self):
		return self.website

	def getEmail(self):
		return self.sp_email_id

	def getFName(self):
		return self.sp_fname

	def getLName(self):
		return self.sp_lname

	def getPassword(self):
		return self.password

	def getPhone(self):
		return self.ph_no

	def setEmail(self, email):
		self.sp_email_id = email
		db.session.commit()

	def setFName(self,fname):
		self.sp_fname = fname
		db.session.commit()

	def setLName(self, lname):
		self.sp_lname = lname
		db.session.commit()

	def setPassword(self, password):
		self.password = password
		db.session.commit()

	def setPhone(self, phone):
		self.ph_no = phone
		db.session.commit()

	def setWebsite(self, website):
		self.website = website
		db.session.commit()

class Location(db.Model):
	__tablename__ = 'location'
	location_id = db.Column(db.Integer, primary_key = True)	# serial datatype need not to provide
	venue_name = db.Column(db.VARCHAR(length = 100), nullable = False)
	adderess_id = db.Column(db.VARCHAR(length = 130), db.ForeignKey('adderess.adderess_id'), nullable = False)
	event1 = db.relationship('Event1', cascade = 'all, delete', backref = db.backref('location', lazy=True))

class Sponser(db.Model):
	__tablename__ = 'sponser'
	semail_id = db.Column(db.VARCHAR(length = 100), primary_key = True)
	s_fname = db.Column(db.VARCHAR(length = 30), nullable = False)
	s_lname = db.Column(db.VARCHAR(length = 30), nullable = False)
	password = db.Column(db.VARCHAR(length = 65), nullable = False)
	ph_no = db.Column(db.VARCHAR(length = 12))
	website = db.Column(db.VARCHAR(length = 50))
	adderess_id = db.Column(db.VARCHAR(length = 130), db.ForeignKey('adderess.adderess_id'), nullable = False)
	event = db.relationship('Event1', secondary = 'sponsers', cascade = 'all, delete', backref = db.backref('have_sponser', lazy = True))

	@staticmethod
	def check_credentials(email, password):
		Uoutput = Sponser.query.filter_by(semail_id = email).first()
		if Uoutput == None:
			return None
		elif Uoutput.password != password :
			return 'PWSNOTMATCHED'
		else:
			return 'PWSMATCHED'

	@staticmethod
	def getDropDown():
		d = {'Profile':"profile", 'History':"history",
			'Notification':"notification", 'Feedback':"feedback",
			'Logout':"logout"}
		return d

	def getWebsite(self):
		return self.website

	def getEmail(self):
		return self.semail_id

	def getFName(self):
		return self.s_fname

	def getLName(self):
		return self.s_lname

	def getPassword(self):
		return self.password

	def getPhone(self):
		return self.ph_no

	def setEmail(self, email):
		self.semail_id = email
		db.session.commit()

	def setFName(self,fname):
		self.s_fname = fname
		db.session.commit()

	def setLName(self, lname):
		self.s_lname = lname
		db.session.commit()

	def setPassword(self, password):
		self.password = password
		db.session.commit()

	def setPhone(self, phone):
		self.ph_no = phone
		db.session.commit()

	def setWebsite(self, website):
		self.website = website
		db.session.commit()


class Event2(db.Model):
	__tablename__ = 'event2'
	e_name_id = db.Column(db.Integer, primary_key = True)
	ename = db.Column(db.VARCHAR(length = 100))
	event1 = db.relationship('Event1', cascade = 'all, delete', backref = db.backref('event2', lazy=True))

class Event1(db.Model):
	__tablename__ = 'event1'
	e_sdate = db.Column(db.TIMESTAMP, primary_key=True)
	location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), primary_key=True)
	e_edate = db.Column(db.TIMESTAMP)
	e_name_id = db.Column(db.Integer, db.ForeignKey('event2.e_name_id'))
	cc_email_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey('company_center.cc_email_id'))
	c_email_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey('client.c_email_id'))
	bill = db.Column(db.JSON)
	dateofregister = db.Column(db.TIMESTAMP, nullable = False)
	ser_id = db.Column(db.JSON)	# is actually a foreign key, but since an object cant refer it
	paid = db.Column(db.Integer)


class Sponsers(db.Model):
	__tablename__ = 'sponsers'
	semail_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey('sponser.semail_id'),primary_key = True)
	e_sdate = db.Column(db.TIMESTAMP, primary_key = True)
	location_id = db.Column(db.Integer, primary_key = True)
	s_donate = db.Column(db.JSON)
	s_dateofreg = db.Column(db.TIMESTAMP)
	sponsershipagreement = db.Column(db.JSON)
	event = db.relationship(Event1, backref = db.backref('sponsers', cascade  = 'all, delete'))
	sponser = db.relationship(Sponser, backref = db.backref('sponsers', cascade  = 'all, delete'))
	__table_args__ = (
						db.ForeignKeyConstraint(
							['e_sdate', 'location_id'],
							['event1.e_sdate', 'event1.location_id']
						,),
					)

class Works_For(db.Model):
	__tablename__ = 'works_for'
	e_sdate = db.Column(db.TIMESTAMP, primary_key = True)
	location_id = db.Column(db.Integer, primary_key = True)
	sp_email_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey('service_provider.sp_email_id'), primary_key = True)
	bill = db.Column(db.JSON)
	paid = db.Column(db.Integer)
	event = db.relationship(Event1, backref = db.backref('works_for', cascade  = 'all, delete'))
	service_provider = db.relationship(Service_Provider, backref = db.backref('works_for', cascade  = 'all, delete'))

	__table_args__ = (
						db.ForeignKeyConstraint(
							['e_sdate', 'location_id'],
							['event1.e_sdate', 'event1.location_id']
						,),
					)

class Comunicatecl(db.Model):
	__tablename__ = 'comunicatec'
	c_email_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey('client.c_email_id'), primary_key = True)
	cc_email_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey('company_center.cc_email_id'), primary_key = True)
	feedback = db.Column(db.JSON)
	client = db.relationship(Client, backref = db.backref('comunicateclref', cascade  = 'all, delete'))
	company_center = db.relationship(Company_Center, backref = db.backref('comunicateclref', cascade  = 'all, delete'))

class Comunicatecc(db.Model):
	__tablename__ = 'comunicatecc'
	ea_email = db.Column(db.VARCHAR(length =50), db.ForeignKey('event_attender.ea_email'), primary_key = True)
	cc_email_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey('company_center.cc_email_id'), primary_key = True)
	feedback = db.Column(db.JSON)
	company_center = db.relationship(Company_Center, backref = db.backref('comunicateccref', cascade  = 'all, delete'))
	event_attender = db.relationship(Event_Attender, backref = db.backref('comunicateccref', cascade  = 'all, delete'))

class Schedule(db.Model):
	__tablename__ = 'schedule'
	e_sdate = db.Column(db.TIMESTAMP, primary_key = True)
	location_id = db.Column(db.Integer, primary_key = True)
	sp_email_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey('service_provider.sp_email_id'), primary_key = True)
	start_date = db.Column(db.TIMESTAMP)
	end_date = db.Column(db.TIMESTAMP)

	__table_args__ = (
						db.ForeignKeyConstraint(
							['e_sdate', 'location_id'],
							['event1.e_sdate', 'event1.location_id']
						,),
					)

class Attends(db.Model):
	__tablename__ = 'attends'

	ea_email = db.Column(db.VARCHAR(length = 50), db.ForeignKey('event_attender.ea_email'), primary_key = True)
	e_sdate = db.Column( db.TIMESTAMP, primary_key = True)
	location_id = db.Column(db.Integer, primary_key=True)
	dateofregistration = db.Column(db.TIMESTAMP, nullable = False)
	ticket = db.Column(db.JSON, nullable = False)
	event = db.relationship(Event1, backref = db.backref('attends', cascade  = 'all, delete'))
	event_attender = db.relationship(Event_Attender, backref = db.backref('attends', cascade  = 'all, delete'))
	__table_args__ = (
						db.ForeignKeyConstraint(
							['e_sdate', 'location_id'],
							['event1.e_sdate', 'event1.location_id']

						,),
					)

class Old_CompanyDatabase(db.Model):
	__tablename__ = 'old_companydb'
	Edate_time = db.Column(db.TIMESTAMP, primary_key = True)
	ssn = db.Column(db.VARCHAR(20), primary_key = True)
	first_name = db.Column(db.VARCHAR(length = 30), nullable = False)
	last_name = db.Column(db.VARCHAR(length = 30), nullable = False)
	designation = db.Column(db.VARCHAR(length = 100), nullable = False)
	cc_email_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey('company_center.cc_email_id'))
	sdate_time = db.Column(db.TIMESTAMP)
	email = db.Column(db.VARCHAR(length = 50), nullable = False)
	password = db.Column(db.VARCHAR(length = 65), nullable = False)
	ph_no = db.Column(db.VARCHAR(length = 12))
	adderess_id = db.Column(db.VARCHAR(length = 130), db.ForeignKey('adderess.adderess_id'), nullable = False)	# dont know how to impliment on delete set null


# CREATE OR REPLACE FUNCTION transfer_old_data()
#   RETURNS trigger AS
# $BODY$
# BEGIN
#    IF NEW.cc_email_id != OLD.cc_email_id THEN
#       INSERT INTO old_companydb VALUES(NOW(), OLD.SSN, OLD.FIRST_NAME, OLD.LAST_NAME, OLD.DESIGNATION, OLD.CC_EMAIL_ID, OLD.SDATE_TIME, OLD.EMAIL, OLD.PASSWORD, OLD.PH_NO, OLD.ADDERESS_ID);
#    END IF;
#    RETURN NEW;
# END;
# $BODY$
# LANGUAGE plpgsql;

# CREATE TRIGGER trigger_to_transfer
# 	BEFORE UPDATE
#  	ON Company_Employee
#  	FOR EACH ROW
#  	EXECUTE PROCEDURE transfer_old_data();

# insert into company_center values('cc@email1.com', '123456789', '2xyz12345');
# insert into company_employee values('123456789', 'Tanishq','Shrivastava','Branch Manager', 'cc@email1.com', NOW(), 'tanishqshrivastava01@gmail.com', 'abc123', '123456789','2xyz12345');
# update company_employee set cc_email_id = 'cc@email2.com' where ssn = '123456789';


