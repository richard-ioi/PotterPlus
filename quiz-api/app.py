import requests
from flask import Flask, request
from flask_cors import CORS
from utils.jwt_utils import build_token
from utils.jwt_utils import decode_token
import service.questionService as questionService
import service.participationService as participationService
import service.quizInfoService as quizInfoService
from model.participation import serialize

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_api():
    x = 'world'
    return f"Hello, {x}"

@app.route('/api')
def hello_world():
    x = 'world'
    return f"Hello, {x}"


@app.route('/api/quiz-info', methods=['GET'])
def GetQuizInfo():
    return quizInfoService.getQuizInfo()


@app.route('/api/login', methods=['POST'])
def SendUserLogin():
    payload = request.get_json()
    if 'Vive l\'ESIEE !' == payload['password']:
        token = build_token()
        return {'token': token}
    else:
        return '', 401


@app.route('/api/questions', methods=['POST'])
def PostQuestion():
    try:
        if (decode_token((request.headers.get('Authorization'))[7:]) == 'quiz-app-admin'):
            question = request.get_json()
            return questionService.checkQuestionPosition(question)
        else:
            return '', 401
    except Exception:
        return '', 401


@app.route('/api/questions/<question_position>', methods=['GET'])
def GetQuestion(question_position):
    return questionService.getQuestionByPosition(question_position)


@app.route('/api/questions/<question_position>', methods=['PUT'])
def UpdateQuestion(question_position):
    try:
        if (decode_token((request.headers.get('Authorization'))[7:]) == 'quiz-app-admin'):
            newQuestion = request.get_json()
            return questionService.updateQuestionByPosition(question_position, newQuestion)
    except Exception:
        return '', 400


@app.route('/api/questions/<question_position>', methods=['DELETE'])
def DeleteQuestion(question_position):
    try:
        if (decode_token((request.headers.get('Authorization'))[7:]) == 'quiz-app-admin'):
            return questionService.deleteQuestionByPosition(question_position)
        else:
            return '', 401
    except Exception:
        return '', 401


@app.route('/api/participations', methods=['POST'])
def SaveParticipation():
    try:
        participationParameters = request.get_json()
        participation = participationService.createParticipation(
            participationParameters)
        quizInfoService.insertScore(participation)
        #headers = {'args': ['richard.fouquoire@gmail.com', 'Résultat de score', participation]}
        json_data = {
            'args': [
                'richard.fouquoire@gmail.com',
                'Résultats de la participation',
                participation.playerName+' a obtenu un score de '+str(participation.score),
            ],
        }
        r = requests.post('http://mail-api-service.default.svc.cluster.local:5000/commands/mail', json=json_data)
        return serialize(participation), 200
    except Exception:
        return '', 400


@app.route('/api/participations', methods=['DELETE'])
def DeleteParticipation():
    try:
        if (decode_token((request.headers.get('Authorization'))[7:]) == 'quiz-app-admin'):
            return quizInfoService.deleteAllQuizInfo()
    except Exception:
        return '', 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, processes=1)
