import json
from flask import Flask, request
from importlib_metadata import method_cache

from utils.jwt_utils import build_token
from utils.jwt_utils import decode_token
import service.questionServices as questionServices
import service.participationService as participationService


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
		return {'token' : token}
	else:
		return '', 401

@app.route('/questions', methods=['POST'])
def PostQuestion():
	try:
		if (decode_token((request.headers.get('Authorization'))[7:])=='quiz-app-admin'):
			question = request.get_json()
			return questionServices.checkQuestionPosition(question)
		else:
			return '',401
	except Exception:
		return '',401
	

@app.route('/questions/<question_position>', methods=['GET'])
def GetQuestion(question_position):
	return questionServices.getQuestionByPosition(question_position)

@app.route('/questions/<question_position>', methods=['PUT'])
def UpdateQuestion(question_position):
	newQuestion = request.get_json()
	return questionServices.updateQuestionByPosition(question_position,newQuestion)

@app.route('/questions/<question_position>', methods=['DELETE'])
def DeleteQuestion(question_position):
	try:
		if (decode_token((request.headers.get('Authorization'))[7:])=='quiz-app-admin'):
			return questionServices.deleteQuestionByPosition(question_position)
		else:
			return '',401
	except Exception:
		return '',401

@app.route('/participations', methods=['POST'])
def SaveParticipation():
	participationParameters = request.get_json()
	participation = participationService.createParticipation(participationParameters)
	#QuizInfoServices.insertScore(participation)
	return json.dumps(participation),200
    	

if __name__ == "__main__":
    app.run(ssl_context='adhoc')