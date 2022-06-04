import json

class QuizInfo():
	def __init__(self, size: int):
		self.size = size
		self.scores = []

	def set_Scores(self, scores):
		self.scores = scores
	
	def serialize(quizInfo):
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
