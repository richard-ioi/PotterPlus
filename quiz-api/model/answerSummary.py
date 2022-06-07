class AnswerSummary():
	"""
	A class used to represent an AnswerSummary
	It's a class with two attributes to know if the answer is correct
	and what's the correctAnswerPosition for a given Question

	Primarly used in the participation object to get a summary of all 
	the answers of a quiz

	Attributes
	------
	correctAnswerPosition : int
		Correct index of the answer
	wasCorrect : bool
		True if the answer is correct, False otherwise
	"""
	def __init__(self, correctAnswerPosition: int, wasCorrect : bool):
		"""
		Parameters
		------
		correctAnswerPosition : int
			Correct index of the answer
		wasCorrect : bool
			True if the answer is correct, False otherwise
		"""
		self.correctAnswerPosition = correctAnswerPosition
		self.wasCorrect = wasCorrect