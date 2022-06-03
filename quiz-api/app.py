import json
from flask import Flask, request
from importlib_metadata import method_cache
from utils.jwt_utils import build_token
from utils.jwt_utils import decode_token
import service.questionService as questionService
import service.participationService as participationService
import service.quizInfoService as quizInfoService
from model.participation import serialize


app = Flask(__name__)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	#return {"size": 0, "scores": []}, 200
	return quizInfoService.getQuizInfo()

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
			return questionService.checkQuestionPosition(question)
		else:
			return '',401
	except Exception:
		return '',401
	

@app.route('/questions/<question_position>', methods=['GET'])
def GetQuestion(question_position):
	return questionService.getQuestionByPosition(question_position)

@app.route('/questions/<question_position>', methods=['PUT'])
def UpdateQuestion(question_position):
	newQuestion = request.get_json()
	return questionService.updateQuestionByPosition(question_position,newQuestion)

@app.route('/questions/<question_position>', methods=['DELETE'])
def DeleteQuestion(question_position):
	try:
		if (decode_token((request.headers.get('Authorization'))[7:])=='quiz-app-admin'):
			return questionService.deleteQuestionByPosition(question_position)
		else:
			return '',401
	except Exception:
		return '',401

@app.route('/participations', methods=['POST'])
def SaveParticipation():
	try:
		participationParameters = request.get_json()
		participation = participationService.createParticipation(participationParameters)
		quizInfoService.insertScore(participation)
		return serialize(participation),200
	except Exception:
		return '',400

@app.route('/participations', methods=['DELETE'])
def DeleteParticipation():
	return quizInfoService.deleteAllQuizInfo()
		
if __name__ == "__main__":
	app.run(ssl_context='adhoc')