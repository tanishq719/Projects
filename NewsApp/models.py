from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class NUser(db.Model):
	__tablename__ = "nuser"
	email_id = db.Column(db.VARCHAR(length = 50), primary_key = True)
	first_name = db.Column(db.VARCHAR(length = 20), nullable = False)
	last_name = db.Column(db.VARCHAR(length = 20), nullable = False)
	password = db.Column(db.VARCHAR(length = 20), nullable = False)
	age = db.Column(db.Integer, nullable = False)
	profession = db.Column(db.VARCHAR(length = 50), nullable = False)
	photo = db.Column(db.LargeBinary)
	feedback = db.Column(db.JSON)
	has_tags = db.relationship('tags', secondary = 'nusertagr', cascade = 'all, delete', backref=db.backref('areof', lazy= True))

	# for tags different table is made

class Tags(db.Model):
	__tablename__ = "tags"
	tag_id = db.Column(db.Integer, primary_key = True)
	tag = db.Column(db.VARCHAR(length = 50), nullable = False)

class NUserTagR(db.Model):
	__tablename__ = 'nusertagr'
	email_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey(NUser.email_id), primary_key = True)
	tag_id = db.Column(db.Integer, db.ForeignKey(Tags.tag_id), primary_key = True)

class Info(db.Model):
	_tablename__ = 'info'

	info_seq_id = db.Column(db.Integer, db.Sequence('info_info_seq_id_seq'), primary_key = True, server_default = db.Sequence('info_info_seq_id_seq').next_value())
	info_datetime_id = db.Column(db.TIMESTAMP, primary_key = True, server_default = 'NOW()')
	title = db.Column(db.Text, nullable = False)
	source_url = db.Column(db.Text, nullable = False)
	tags = db.Column(db.VARCHAR(10), nullable = False)	# cant be declared as foreign key, as multivalues attribute
	content = db.Column(db.JSON, nullable = False)

	possess_by = db.relationship('nuser', secondary = 'access', backref = db.backref('has_Info', lazy = True))

	tdate = ""
	def __init__(self, **kwargs):
		super(Info, self).__init__(**kwargs)
		if( tdate == ""):
			tdate = str(date.today())
		elif(tdate != str(date.today())):
			db.engine.execute('ALTER SEQUENCE info_info_seq_id_seq RESTART')

class Access(db.Model):			# insertion will take place only when user want to save this news for himself or like it
	__tablename__ = 'access'

	email_id = db.Column(db.VARCHAR(length = 50), db.ForeignKey(NUser.email_id),primary_key = True)
	info_seq_id = db.Column(db.Integer, primary_key = True)
	info_datetime_id = db.Column(db.TIMESTAMP, primary_key = True)

	__table_args__ = (
		db.ForeignKeyConstraint(
			['info_seq_id', 'info_datetime_id'],
			['info.info_seq_id', 'info.info_datetime_id'],
			ondelete = 'CASCADE',),
		)

