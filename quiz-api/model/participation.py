import json

class Participation():
	"""
	A class used to represent a Participation model,
	primarly used to know score informations on a given playerName
	with a given answer indexes array

	Attributes
	------
	playerName : str
		Name of the player
	score : int
		Score of the player
	answerSummaries : tuple
		Array of answerSummary objects used to summarize the answers indexes of the player's game
	"""
	def __init__(self, playerName: str, score: int):
		"""
		Parameters
		------
		playerName : str
			Name of the player
		score : int
			Score of the player
		"""
		self.playerName = playerName
		self.score = score 
		self.answersSummaries = []
	
	def set_AnswerSummaries(self, answersSummaries):
		"""
		A method used to set the AnswerSummaries tuple of the Participation

		Parameters
		------
		answerSummaries : tuple
			Tuple of AnswerSummaries
		"""
		self.answersSummaries = answersSummaries

def serialize(participation):
	"""
	A method used to transform the Participation object informations
	into a json object 

	Parameters
	------
	participation : Participation object
		Participation object needed to be serialized
	
	Returns
	------
	json object
		The participation attributes serialized in a json object
	"""
	data = {
		"answerSummaries":[],
		"playerName":participation.playerName,
		"score":participation.score
	}
	for answerSummary in participation.answersSummaries:
		answerSummaryData= {
			"correctAnswerPosition":answerSummary.correctAnswerPosition,
			"wasCorrect":answerSummary.wasCorrect
		}
		data["answerSummaries"].append(answerSummaryData)
	return json.dumps(data)
