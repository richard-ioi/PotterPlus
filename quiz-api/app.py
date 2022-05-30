from flask import Flask, request
from importlib_metadata import method_cache

from utils.jwt_utils import build_token
from utils.jwt_utils import decode_token
import service.questionServices as questionServices
import service.loginService as loginServices
import sqlite3

app = Flask(__name__)

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
	return questionServices.createQuestion(question)

@app.route('/questions/<question_id>', methods=['GET'])
def GetQuestion(question_id):
	return questionServices.getQuestionByID(question_id)

@app.route('/questions/<question_id>', methods=['PUT'])
def UpdateQuestion(question_id):
	newQuestion = request.get_json()
	return questionServices.updateQuestionByID(question_id,newQuestion)

@app.route('/questions/<question_id>', methods=['DELETE'])
def DeleteQuestion(question_id):
	return questionServices.deleteQuestionByID(question_id)
    	

if __name__ == "__main__":
    app.run(ssl_context='adhoc')