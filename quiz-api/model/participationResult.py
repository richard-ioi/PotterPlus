from datetime import date

class ParticipationResult():
	"""
	A class used to represent a ParticipationResult
	It's a class with three attributes which summaries a game of a player
	with its name, score and date of the game

	Primarly used in the quizInfo object

	Attributes
	------
	playerName : str
		Name of the player
	score : int
		Score of the player
	date : date
		Date of the game
	"""
	def __init__(self, playerName: int, score : int, date : date):
		"""
		Parameters
		------
		playerName : str
			Name of the player
		score : int
			Score of the player
		date : date
			Date of the game	
		"""
		self.playerName = playerName
		self.score = score
		self.date = date
