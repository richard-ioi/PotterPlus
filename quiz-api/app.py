from flask import Flask, request
import jwt_utils

app = Flask(__name__)

token = ''

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def CheckLogin():
	payload = request.get_json()
	if(payload['password']=="Vive l'ESIEE !"):
		token = jwt_utils.build_token()
		return { 'token' : token }
	else:
		return '', 401

@app.route('/questions', methods=['POST'])
def PostQuestion():
	CheckAdmin()

def CheckAdmin():
	if(jwt_utils.decode_token(request.headers.get('Authorization'))!='quiz-app-admin'):
		return '', 401


if __name__ == "__main__":
    app.run(ssl_context='adhoc')