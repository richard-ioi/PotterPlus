import json
from model.answer import Answer
from utils.dbUtils import connectDB

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
    print("InsertAnswer ",  answer.id, answer.text, answer.isCorrect)
    if answer.id != -1:
        request =  f'INSERT INTO answer(ID, QUESTION_ID, TEXT, is_Correct) VALUES ({answer.id},{answer.questionID},"{answer.text}", {answer.isCorrect});'
        return request
    else:
        request =  f'INSERT INTO answer(QUESTION_ID, TEXT, IS_CORRECT) VALUES ({answer.questionID},"{answer.text}", {answer.isCorrect});'
        return request

def getAnswerByQuestionID(questionID):
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    request = "SELECT * FROM ANSWER WHERE QUESTION_ID ="+questionID+" ORDER BY ID;"
    answers = []
    try:
        cursor.execute(request)
        rows = cursor.fetchall()
        for row in rows:
            id=row[0]
            text = row[2]
            isCorrect = row[3]
            answers.append(Answer(id,questionID,text,isCorrect))
            
        return answers
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        raise err