from flask_sqlalchemy import SQLAlchemy
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

class Company_Employee(db.Model):
	__tablename__ = 'company_employee'
	ssn = db.Column(db.VARCHAR(20), primary_key = True)
	first_name = db.Column(db.VARCHAR(length = 30), nullable = False)
	last_name = db.Column(db.VARCHAR(length = 30), nullable = False)
	email = db.Column(db.VARCHAR(length = 50), nullable = False)
	password = db.Column(db.VARCHAR(length = 65), nullable = False)
	ph_no = db.Column(db.VARCHAR(length = 12))
	adderess_id = db.Column(db.VARCHAR(length = 130), db.ForeignKey('adderess.adderess_id'), nullable = False)	# dont know how to impliment on delete set null
	

class Company_Center(db.Model):
	__tablename__ = 'company_center'
	cc_email_id = db.Column(db.VARCHAR(length = 50), primary_key = True)
	manager_id = db.Column(db.VARCHAR(length = 20), db.ForeignKey('company_employee.ssn'))
	eplanar_id = db.Column(db.VARCHAR(length = 20), db.ForeignKey('company_employee.ssn'))
	ticketsalesmg_id = db.Column(db.VARCHAR(length = 20), db.ForeignKey('company_employee.ssn'))
	ph_no = db.Column(db.VARCHAR(length = 12))
	adderess_id = db.Column(db.VARCHAR(length = 130), db.ForeignKey('adderess.adderess_id'), nullable = False)	
	event1 = db.relationship('Event1', cascade = 'all, delete', backref =db.backref('company_center', lazy=True))

class Services(db.Model):
	__tablename__ = 'services'
	ser_id = db.Column(db.Integer, primary_key = True)
	service_name = db.Column(db.VARCHAR(length = 100))
	service_provider = db.relationship('Service_Provider', cascade = 'all, delete', backref = db.backref('services', lazy=True))	# uselist is not set to false because relationship here is one to many

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