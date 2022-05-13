from flask import Flask, request
import jwt_utils

app = Flask(__name__)

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
	print(payload['password'])
	if(payload['password']=="Vive l'ESIEE !"):
		return jwt_utils.build_token()
	else:
		return '', 401

if __name__ == "__main__":
    app.run(ssl_context='adhoc')