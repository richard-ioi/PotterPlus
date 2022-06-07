import json
from model.answer import Answer


class Question():
    """
    A class used to represent a Question.

    ...

    Attributes
    ----------
    id : int
        the question id
    title : string
        the title of the question
    text : string
        the question text
    image : string
        the base64 image code
    positon : int
        the position of the question in the quiz
    possibleAnswers : list
        the list of possible answers

    Methods
    -------
    set_possibleAnswers(self, possibleAnswers)
        sets the possible answers for a question.
    
    isQuestionValid(question):
        checks if the question has all not null fields filled.
    
    serialize(question):
        serializes the question to JSON.
    
    deserialize(dbJson):
        deserializes json to Question.

    getCorrectAnswerPosition(Question);
        gets correct answer position for the question.
    """
    def __init__(self, id: int, title: str, text: str, image: str, position: int):
        self.id = id
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.possibleAnswers = []

    def set_possibleAnswers(self, possibleAnswers):
        """Sets the possible answers for a question.
        """
        self.possibleAnswers = possibleAnswers

    def IsQuestionValid(question):
        """Checks if the question has all not null fields filled.
        
        Parameters
        -------
        question
            The question.

        Returns
        -------
        boolean
            True is the question is valid. Else False.

        """
        if not question['text'] or not question['title'] or not question['position']:
            return False
        return True

    def serialize(question):
        """Serializes the question to JSON.

        Returns
        -------
        json
            The serialized question.
        """
        data = {
            "text": question.text,
            "title": question.title,
            "image": question.image,
            "position": int(question.position),
            "possibleAnswers": []
        }
        for answer in question.possibleAnswers:
            isCorrect = True
            if(answer.isCorrect == 0):
                isCorrect = False
            answerData = {
                "id": answer.id,
                "questionID": answer.questionID,
                "text": answer.text,
                "isCorrect": isCorrect
            }
            data["possibleAnswers"].append(answerData)

        return json.dumps(data)

    def deserialize(dbJson: json):
        """Deserializes json to Question.
        
        Returns
        -------
        json
            The deserialized question.
        """
        title = dbJson["title"]
        text = dbJson["text"]
        image = dbJson["image"]
        position = dbJson["position"]
        print("Position", position)
        if "id" in dbJson:
            id = dbJson["id"]
            question = Question(id, title, text, image, position)
        else:
            question = Question(-1, title, text, image, position)

        answers = []
        for answer in dbJson["possibleAnswers"]:
            answers.append(Answer.deserialize(question.id, answer))
        question.set_possibleAnswers(answers)

        return question

    def getCorrectAnswerPosition(Question):
        """Gets correct answer position for the question.
        Returns
        -------
        int
            The correct answer position.
        """
        i = 0
        for answer in Question.possibleAnswers:
            if(answer.isCorrect == 1):
                return i
            i += 1
