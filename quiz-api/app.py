from flask import Flask, request
from importlib_metadata import method_cache

from utils.jwt_utils import build_token
from utils.jwt_utils import decode_token
import service.questionServices as questionServices

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
		token=build_token()
		print(token)
		return {'token' : token}
	else:
		return '', 401

@app.route('/questions', methods=['POST'])
def PostQuestion():
	try:
		if (decode_token((request.headers.get('Authorization'))[7:])=='quiz-app-admin'):
			question = request.get_json()
			return questionServices.createQuestion(question)
		else:
			return '',401
	except Exception:
		return '',401
	

@app.route('/questions/<question_id>', methods=['GET'])
def GetQuestion(question_id):
	return questionServices.getQuestionByID(question_id)

@app.route('/questions/<question_id>', methods=['PUT'])
def UpdateQuestion(question_id):
	try:
		if (decode_token((request.headers.get('Authorization'))[7:])=='quiz-app-admin'):
			newQuestion = request.get_json()
			return questionServices.updateQuestionByID(question_id,newQuestion)
		else:
			return '',401
	except Exception:
		return '',401

@app.route('/questions/<question_id>', methods=['DELETE'])
def DeleteQuestion(question_id):
	try:
		if (decode_token((request.headers.get('Authorization'))[7:])=='quiz-app-admin'):
			return questionServices.deleteQuestionByID(question_id)
		else:
			return '',401
	except Exception:
		return '',401
    	

if __name__ == "__main__":
    app.run(ssl_context='adhoc')