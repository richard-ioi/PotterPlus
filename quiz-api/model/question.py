# Exemple de création de classe en python
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