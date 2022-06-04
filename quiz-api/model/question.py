# Exemple de création de classe en python
import json
from model.answer import Answer

class Question():
	def __init__(self, id:int, title: str, text: str, image: str, position: int):
		self.id = id
		self.title = title
		self.text = text
		self.image = image 
		self.position = position
		self.possibleAnswers = []
	
	def set_possibleAnswers(self, possibleAnswers):
		self.possibleAnswers = possibleAnswers

	def IsQuestionValid(question):
		if not question['text'] or not question['title'] or not question['position']:
			return False
		return True


	def serialize(question):
		data = {
			"text":question.text,
			"title":question.title,
			"image":question.image,
			"position":int(question.position),
			"possibleAnswers":[]
		}
		for answer in question.possibleAnswers:
			isCorrect=True
			if(answer.isCorrect==0):
				isCorrect=False
			answerData = {
				"id":answer.id,
				"questionID":answer.questionID,
				"text":answer.text,
				"isCorrect":isCorrect
			}
			data["possibleAnswers"].append(answerData)

		return json.dumps(data)
		
	def deserialize(dbJson: json):  
		title = dbJson["title"]
		text = dbJson["text"]
		image = dbJson["image"]
		position = dbJson["position"]
		print("Position", position)
		if "id" in dbJson:
			id = dbJson["id"]
			question = Question(id, title, text, image, position)
		else:
			question = Question(-1, title, text, image, position)
			
		answers = []
		for answer in dbJson["possibleAnswers"]:
			answers.append(Answer.deserialize(question.id, answer))
		question.set_possibleAnswers(answers)

		return question
	
	def getCorrectAnswerPosition(Question):
		i=0
		for answer in Question.possibleAnswers:
			if(answer.isCorrect==1):
				return i
			i+=1