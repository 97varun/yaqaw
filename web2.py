from flask import Flask, jsonify
from flask import request, render_template
import json
import pickle
from flask_cors import CORS
import pymongo
from pprint import pprint
import hashlib
from bson import ObjectId
app = Flask(__name__)
json_decoder = json.JSONDecoder()
json_encoder = json.JSONEncoder()
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = my_client["webdb"]
# my_client.drop_database('webdb')
USERTABLE = mydb["USERTABLE"]
posts = mydb["posts"]
QanA = mydb['QandA']

session = {'username' : ''}
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/questions', methods=['GET'])
def questions():
   	return render_template('question.html')

@app.route('/profile', methods=['GET'])
def profile():
	return render_template('profile.html')

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html')

@app.route('/register', methods=['GET'])
def register():
	return render_template('register.html')

@app.route('/checkuser', methods = ['POST'])
def check_user():
	username = request.json['username']
	password = request.json['password']
	doc = USERTABLE.find_one({'username' : username})
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

@app.route('/adduser', methods = ['POST'])
def add_user():
	username = request.json['username']
	password = request.json['password']
	about = request.json['about']
	obj = {'username' : username, 'password' : hashlib.md5(password.encode()).hexdigest(), "about" : about}
	USERTABLE.insert_one(obj)
	return json_encoder.encode({"message":"Success"})

@app.route('/getinfo', methods = ['POST'])
def get_info():
	username = session['username']
	username = 'gb'
	x = USERTABLE.find_one({'username':username})
	about = x['about']
	print(x)
	try :
		return json_encoder.encode({"username" : username,"about": about})
	except :
		return json_encoder.encode({"username" : username,"about": about})

@app.route('/addquestion', methods = ['POST'])		
def add_question():
	question = request.json['question']
	global session
	# session['username']="abc"
	if(session['username']):	
		username=session['username']

		result = posts.insert({"question":question,"username":username})
		if(result):
			return json_encoder.encode({"status":"success"})
		else:
			return json_encoder.encode({"status":"failed"})
	else:
		return json_encoder.encode({"error":"need to be logged in"})

@app.route('/addanswer', methods = ['POST'])
def add_answer():
	question = request.json['question']
	answer = request.json['answer']
	try :
		posts.update({'question': question}, {'$push' : {'answers' : [answer,[''],[''],session['username']]}}, upsert=True)
		return json_encoder.encode({"message":"Success"})
	except :
		return json_encoder.encode({"message":"Failure in add_answer"})

@app.route('/vote', methods = ['POST'])
def vote():
	answer = request.json['answer']
	username = request.json['username']
	type_vote = request.json['vote']
	# question = request.json['question']  'question' : question 
	id_q = request.json['id'] 
	x = posts.find_one({'_id' : id_q})
	idx = 0
	for i in x['answers']:	
		if(i[0] == answer):
			y = i
			break
		else:
			idx += 1	
	if(type_vote == 'upvote'):
		if username not in y[1]:
			y[1].append(username)
	else:
		if username not in y[2]:
			y[2].append(username)
	posts.update({'_id' : id_q}, {"$set" : {'answers.'+str(idx) : y}}, upsert=True)	
	return json_encoder.encode({'upvote' : len(y[1])-1, 'downvote' : len(y[2])-1})		

@app.route('/getquestions', methods = ['GET'])
def	getquestions():
	global session
	username = session['username']
	username="gb"
	if(username):
		doc =list(posts.find({"username":username}))
		docarr=[]
		for i in doc :
			docarr.append(i)
		return JSONEncoder().encode(docarr)
	else:
		return json_encoder.encode({"error":"need to be logged in"})

@app.route('/getanswers', methods = ['GET'])
def	get_answers():
	global session
	username = session['username']
	username="abc"
	if(username):
		docs =list(posts.find())
		docarr=[]

		for doc in docs:
			ans = list(filter(lambda x: x[3] == username, doc['answers']))
			if len(ans):
				doc['answers'] = ans
				docarr.append(doc)
				
		return JSONEncoder().encode(docarr)
	else:
		return json_encoder.encode({"error":"need to be logged in"})

@app.route('/search', methods = ['POST'])
def search_query():
	query = request.json['query']
	results = posts.find({'$text': {'$search': query}}, {'score': {'$meta': 'textScore'}})
	print(results)
	docarr=[]
	for i in results:
		docarr.append(i)
	return JSONEncoder().encode(docarr)
	
@app.route('/logout')
def logout():
	session['username'] = ''
	return render_template('login.html')

if __name__ == '__main__':
   app.run(debug = True)