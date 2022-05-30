import json
from model.answer import Answer

def serialize(answer: Answer):
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

def insertAnswerRequest(answer: Answer):
    if answer.id != -1:
        request =  f'INSERT INTO answer(ID, QUESTION_ID, TEXT, is_Correct) VALUES ({answer.id},{answer.questionID},"{answer.text}", {answer.isCorrect});'
        return request
    else:
        request =  f'INSERT INTO answer(QUESTION_ID, TEXT, IS_CORRECT) VALUES ({answer.questionID},"{answer.text}", {answer.isCorrect});'
        return request