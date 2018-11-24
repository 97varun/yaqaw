import json
import pickle
import pymongo
import hashlib
from bson import ObjectId
from pprint import pprint
from flask_cors import CORS
from mysummarizer import ExtractiveSummarizer
from flask import Flask, jsonify, request, render_template,redirect
import random
app = Flask(__name__)
json_decoder = json.JSONDecoder()
json_encoder = json.JSONEncoder()
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = my_client["webdb"]
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
	if(not session['username']):
		return redirect('/login')
	return render_template('question.html')

@app.route('/profile', methods=['GET'])
def profile():
	if(not session['username']):
		return redirect('/login')
	
	return render_template('profile.html')

@app.route('/login', methods=['GET'])
def login():
	if(request.method=="GET"):
		return render_template('login.html')
	#else:


@app.route('/register', methods=['GET'])
def register():
	return render_template('register.html')

@app.route('/login', methods = ['POST'])
def check_user():
	#return json_encoder.encode({"message":"Failure", "comment":"User not registered"})	
	username = request.json['username']
	password = request.json['password']
	doc = USERTABLE.find({'username' : username})
	

	if(doc.count()):
		doc =list(doc)[0]
		if(doc['password'] == hashlib.md5(password.encode()).hexdigest()):
			global session
			session['username'] = username
			return json_encoder.encode({"message":"Success", "comment":"Username and password match"})
		else:
			return json_encoder.encode({"message":"Failure", "comment":"Username and password doesn't match"})
	else:
		return json_encoder.encode({"message":"Failure", "comment":"User not registered"})	

@app.route('/register', methods = ['POST'])
def add_user():
	username = request.json['username']
	password = request.json['password']
	about = request.json['about']
	obj = {'username' : username, 'password' : hashlib.md5(password.encode()).hexdigest(), "about" : about}
	USERTABLE.insert_one(obj)

	return json_encoder.encode({"message":"Success"})

@app.route('/getinfo', methods = ['GET'])
def get_info():
	if(not session['username']):
		return redirect('/login');
	username = session['username']
	x = USERTABLE.find_one({'username':username})
	about = x['about']
	try :
		return json_encoder.encode({"username" : username,"about": about})
	except :
		return json_encoder.encode({"username" : username,"about": about})

@app.route('/addquestion', methods = ['POST'])	
def add_question():
	question = request.json['question']
	global session
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
		return json_encoder.encode({"status":"success"})
	except :
		return json_encoder.encode({"status":"failed"})

@app.route('/vote', methods = ['POST'])
def vote():
	answer = request.json['answer']
	username = session['username']
	type_vote = request.json['vote']
	# question = request.json['question']  'question' : question 
	id_q = request.json['id'] 
	x = posts.find_one({'_id': ObjectId(id_q)})
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
	posts.update({'_id' : ObjectId(id_q)}, {"$set" : {'answers.'+str(idx) : y}}, upsert=True)
	return json_encoder.encode({'username' : username, 'type' : type_vote,'answer' : y})		

@app.route('/getquestions', methods = ['GET'])
def	getquestions():
	global session
	type= request.args.get('type')
	username = session['username']
	
	if(type is None):
		query={"username":username}
	else:
		query={}
	
	if(username):
		doc =list(posts.find(query))
		docarr=[]
		for i in doc :
			docarr.append(i)
		random.shuffle(docarr)
		return JSONEncoder().encode(docarr)
	else:
		return json_encoder.encode({"error":"need to be logged in"})

@app.route('/getanswers', methods = ['GET'])
def	get_answers():
	global session
	username = session['username']
	if(username):
		docs = list(posts.find({}))
		docarr=[]
		for doc in docs:
			try:
				ans = list(filter(lambda x: x[3] == username, doc['answers']))
				if len(ans):
					print(doc)
					doc['answers'] = ans
					docarr.append(doc)
			except KeyError:
				pass
		return JSONEncoder().encode(docarr)
	else:
		return json_encoder.encode({"error":"need to be logged in"})

@app.route('/search', methods = ['POST'])
def search_query():
	query = request.json['query']
	results = posts.find({'$text': {'$search': query}}, {'score': {'$meta': 'textScore'}})
	results.sort([('score', {'$meta': 'textScore'})])
	docarr=[]
	for i in results:
		docarr.append(i)
	return JSONEncoder().encode(docarr)
	
@app.route('/logout')
def logout():
	session['username'] = ''
	return render_template('login.html')

@app.route('/getsummary', methods =['GET'])
def summary():
	text = request.args.get('answer')
	return ExtractiveSummarizer().summarizer(text, sentence_count = 2)

if __name__ == '__main__':
   app.run(debug = True)
