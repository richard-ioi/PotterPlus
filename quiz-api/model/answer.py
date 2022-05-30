# Exemple de création de classe en python
from cgitb import text


class Answer():
	def __init__(self, id:int, questionID:int,  text: str, isCorrect: int):
		self.id = id
		self.questionID = questionID
		self.text = text
		self.isCorrect = isCorrect 
