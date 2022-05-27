from flask import Flask, request
from importlib_metadata import method_cache

from jwt_utils import build_token
import service.questionServices as questionServices
import sqlite3

app = Flask(__name__)

#création d'un objet connection
db_connection = sqlite3.connect('../db.db')
# set the sqlite connection in "manual transaction mode"
# (by default, all execute calls are performed in their own transactions, not what we want)
db_connection.isolation_level = None

# start transaction
sqlite3.cursor.execute("begin")

# save the question to db
insertion_result = cur.execute(
	f"insert into Question (title) values"
	f"('{input_question.title}')")

#send the request
sqlite3.cursor.execute("commit")

#in case of exception, roolback the transaction
sqlite3.cursor.execute('rollback')


@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def SendUserLogin():
	payload = request.get_json()
	if 'Vive l\'ESIEE !' == payload['password']:
		return {'token' : build_token()}
	else:
		return '', 401

@app.route('/questions', methods=['POST'])
def PostQuestion():
    #Récupérer le token envoyé en paramètre
	request.headers.get('Authorization')
	#récupèrer un l'objet json envoyé dans le body de la requète
	question = request.get_json()

	if questionServices.IsQuestionValid(question):
		return questionServices.serialize(question)
	else:
		return '', 401
    	

if __name__ == "__main__":
    app.run(ssl_context='adhoc')