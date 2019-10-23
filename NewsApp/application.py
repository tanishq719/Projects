from flask import Flask, render_template, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *
from newsapi import NewsApiClient


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tanishq719@localhost/newsapp'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db.init_app(app)
newsapi = NewsApiClient(api_key='50efcf8d785248c0bde9ae63213c7b32')





@app.route('/')
def index():
	db.create_all();
	# tag1 = Tags(tag = 'business')
	# tag2 = Tags(tag = 'technology')
	# tag3 = Tags(tag = 'gaming')
	# tag4 = Tags(tag = 'sports')
	# tag5 = Tags(tag = 'education')

	# user1 = NUser('qwe@gmail.com','rahul','jain', '12345', '18', 'Student', )
	return render_template('index.html')

@app.route('/getNews')
def getNews():
	# print(newsapi.get_sources())
	list = [{'title':'Iphone launched',
			'tag':'Technology', 'image':'#', 
			'text':'new iphone 11 launched, with latest features', 
			'time':'25 min ago', 
			'link':'https://timesofindia.indiatimes.com/'}]
	return jsonify({"length":10, "content" : list})


if __name__ == "__main__":
	app.run(debug = True)