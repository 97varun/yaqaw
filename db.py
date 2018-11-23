import pymongo
import hashlib
from pprint import pprint

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = my_client["webdb"]
my_client.drop_database('webdb')
USERTABLE = mydb["USERTABLE"]
posts = mydb["posts"]

users = [{'username' : 'admin', 'password' : hashlib.md5('admin'.encode()).hexdigest(), "about" : "I am admin"}]
questions = [{"question" : "what is quora ?","username" : 'Human'}]
answers = [{'question':'what is quora ?','answer' : 'It is question answer website', 'username' : 'God'}]

for i in users:
	USERTABLE.insert_one(i)
for i in questions:
	posts.insert_one(i)
for i in answers:
	posts.update({'question': i['question']}, {'$push' : {'answers' : [i['answer'],[''],[''],i['username']]}}, upsert=True)	

x = USERTABLE.find()
for i in x:
	pprint(i)
x = posts.find()	
for i in x:
	pprint(i)	