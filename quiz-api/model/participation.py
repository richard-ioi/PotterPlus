import json

class Participation():
	def __init__(self, playerName: str, score: int):
		self.playerName = playerName
		self.score = score 
		self.answersSummaries = []
	
	def set_AnswerSummaries(self, answersSummaries):
		self.answersSummaries = answersSummaries

def serialize(participation):
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
