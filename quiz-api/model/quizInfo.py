import json

class QuizInfo():
	"""
	A class used to represent a QuizInfo model,
	Primarly used to know all the score informations of all the players

	Attributes
	------
	size : int
		Number of the players that have participated to the quiz
	score : tuple
		tuple of participationResults which summaries players' games informations such as score, etc.
	"""
	def __init__(self, size: int):
		"""
		Parameters
		------
		size : int
			Number of the players that have participated to the quiz
		"""
		self.size = size
		self.scores = []

	def set_Scores(self, scores):
		"""
		A method used to set the Scores array of the QuizInfo

		Parameters
		------
		scores : tuple
			Tuple of ParticipationResult
		"""
		self.scores = scores
	
	def serialize(quizInfo):
		"""
		A method used to transform the QuizInfo object informations
		into a json object 

		Parameters
		------
		quizInfo : QuizInfo object
			QuizInfo object needed to be serialized
		
		Returns
		------
		json object
			The QuizInfo attributes serialized in a json object
		"""
		data = {
			"size":quizInfo.size,
			"scores":[]
		}
		for participationResult in quizInfo.scores:
			participationResultData = {
				"playerName":participationResult.playerName,
				"score":participationResult.score,
				"date":participationResult.date
			}
			data["scores"].append(participationResultData)
		return json.dumps(data)
