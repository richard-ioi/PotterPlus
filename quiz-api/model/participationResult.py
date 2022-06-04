from datetime import date

class ParticipationResult():
	def __init__(self, playerName: int, score : int, date : date):
		self.playerName = playerName
		self.score = score
		self.date = date
