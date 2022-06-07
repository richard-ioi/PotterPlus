import json

class Answer():
	"""
    A class used to represent a Question.

    ...

    Attributes
    ----------
    id : int
        the answer id
    questionID : string
        the id of the associated question
    text : string
        the answer text
    isCorrect : boolean
        the answer value
   
    Methods
    -------    
    serialize(question):
        serializes the answer to JSON.
    
    deserialize(dbJson):
        deserializes json to Answer.
    """

	def __init__(self, id:int, questionID:int,  text: str, isCorrect: int):
		self.id = id
		self.questionID = questionID
		self.text = text
		self.isCorrect = isCorrect 

	def serialize(answer):
		print(json.dumps(answer.__dict__))
		return json.dumps(answer.__dict__)

	def deserialize(answerID: int, answer: json):
		text = answer["text"]
		isCorrect = answer["isCorrect"]

		if "id" in answer:
			id = answer["id"]
			return Answer(id, answerID, text, isCorrect)
		else:
			return Answer(-1, answerID, text, isCorrect)