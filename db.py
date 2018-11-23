import pymongo
import hashlib
from pprint import pprint

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = my_client["webdb"]
my_client.drop_database('webdb')
USERTABLE = mydb["USERTABLE"]
posts = mydb["posts"]

users = [
	{'username' : 'admin', 'password' : hashlib.md5('admin'.encode()).hexdigest(), "about" : "I am admin"},
	{'username' : 'Human1', 'password' : hashlib.md5('Human1'.encode()).hexdigest(), "about" : "I am Human1"},
	{'username' : 'Human2', 'password' : hashlib.md5('Human2'.encode()).hexdigest(), "about" : "I am Human2"},
	{'username' : 'Human3', 'password' : hashlib.md5('Human3'.encode()).hexdigest(), "about" : "I am Human3"},
	{'username' : 'Human4', 'password' : hashlib.md5('Human4'.encode()).hexdigest(), "about" : "I am Human4"}
]

questions = [
	{"question" : "what is quora ?","username" : 'Human1'}, 
	{"question" : "what is meaning of life ?","username" : 'Human2'},
	{"question" : "how did jesus get his job ?","username" : 'Human3'},
	{"question" : "Why does PESU suck ?","username" : 'Human4'}
]

answers = [
	{'question':'what is quora ?','answer' : 'It is question answer website', 'username' : 'Human2','upvote' : ['','a','b','c'],'downvote' : ['','d','e','f']},
	{'question':'what is quora ?','answer' : 'It is answer question website', 'username' : 'Human3','upvote' : ['','a','b','c'],'downvote' : ['','d','e','f']},
	{'question':'what is meaning of life ?','answer' : 'Nothing', 'username' : 'Human1','upvote' : ['','a','b','c'],'downvote' : ['','d','e','f']},
	{'question':'what is meaning of life ?','answer' : '42', 'username' : 'Human2','upvote' : ['','a','b','c'],'downvote' : ['','d','e','f']},
	{'question':'how did jesus get his job ?','answer' : 'Nepotism', 'username' : 'Human3','upvote' : ['','a','b','c'],'downvote' : ['','d','e','f']},
	{'question':'how did jesus get his job ?','answer' : 'Hard Work', 'username' : 'Human4','upvote' : ['','a','b','c'],'downvote' : ['','d','e','f']},
	{'question':'Why does PESU suck ?','answer' : 'No', 'username' : 'Human1','upvote' : ['','a','b','c'],'downvote' : ['','d','e','f']},
	{'question':'Why does PESU suck ?','answer' : 'Yes', 'username' : 'Human4','upvote' : ['','a','b','c'],'downvote' : ['','d','e','f']}
	
]

for i in users:
	USERTABLE.insert_one(i)
for i in questions:
	posts.insert_one(i)
for i in answers:
	posts.update({'question': i['question']}, {'$push' : {'answers' : [i['answer'],i['upvote'],i['downvote'],i['username']]}}, upsert=True)	

posts.create_index([('question', pymongo.TEXT)])
x = USERTABLE.find()
for i in x:
	pprint(i)
x = posts.find()	
for i in x:
	pprint(i)	