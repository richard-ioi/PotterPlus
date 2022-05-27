# Exemple de création de classe en python
class Question():
	def init(self, title: str, text: str, image: str, position: int, possibleAnswers):
		self.title = title
		self.text = text
		self.image = image 
		self.position = position
		self.possibleAnswers = possibleAnswers