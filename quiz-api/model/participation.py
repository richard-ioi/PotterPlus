class Participation():
	def __init__(self, playerName: str, score: int):
		self.playerName = playerName
		self.score = score 
		self.answersSummaries = []
	
	def set_AnswerSummaries(self, answers):
		self.answers = answers