from flask import Flask
from flask import request
import json
import pickle
from flask_cors import CORS
import pymongo
import pprint
import hashlib
app = Flask(__name__)
json_decoder = json.JSONDecoder()
json_encoder = json.JSONEncoder()
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = my_client["webdb"]
USERTABLE = mydb["USERTABLE"]
posts = mydb["posts"]
QanA = mydb['QandA']

session = {'username' : ''}

@app.route('/')
def hello():
   return 

@app.route('/login', methods = ['POST'])
def login():
	username = request.json['username']
	password = request.json['password']
	doc = USERTABLE.find_one({'username' : username});
	print(doc)
	if(doc):
		if(doc['password'] == hashlib.md5(password.encode()).hexdigest()):
			global session
			session['username'] = username
			return json_encoder.encode({"message":"Success", "comment":"Username and password match"})
		else:
			return json_encoder.encode({"message":"Failure", "comment":"Username and password doesn't match"})
	else:
		return json_encoder.encode({"message":"Failure", "comment":"User not registered"})	

	# if(USERTABLE.find({'username' : username}).count()):
	# 	if(USERTABLE.find({"username" : username, "password": hashlib.md5(password)}).count()):
	# 		global session 
	# 		session['username'] = username
	# 		return json_encoder.encode({"message":"Success", "comment":"Username and password match"})
	# 	return json_encoder.encode({"message":"Failure", "comment":"Username and password doesn't match"})	
	# else:
	# 	return json_encoder.encode({"message":"Failure", "comment":"User not registered"})

@app.route('/register', methods = ['POST'])
def add_user():
	username = request.json['username']
	password = request.json['password']
	obj = {'username' : username, 'password' : hashlib.md5(password.encode()).hexdigest()}
	USERTABLE.insert_one(obj)
	return json_encoder.encode({"message":"Success"})
@app.route('/getinfo', methods = ['GET'])
def get_info():
	username = request.args.get('username');
	x = USERTABLE.find_one({'username':username})
	print(x)
	try :
		return json_encoder.encode({"q_num":len(x['questions']),"a_num":len(x['answers'])})
	except :
		return json_encoder.encode({"q_num":0,"a_num":0})


@app.route('/addquestion', methods = ['POST'])		
def add_question():
	question = request.json['question']
	global session
	username=session['username']
	result = posts.update({"question":question},{"$set":{"username":username}},upsert=True)
	return json_encoder.encode(result);


@app.route('/getinfo', methods = ['GET'])
	global session

	username = session['username']
	if(username):
		posts =posts.find({"username":username})
	



if __name__ == '__main__':
   app.run(debug = True)