import json
from utils.dbUtils import connectDB
from model.question import Question
from model.answer import Answer
import service.answerService as answerService


def IsQuestionValid(question):
    if not question['text'] or not question['title'] or not question['position']:
        return False
    return True


def serialize(question: Question):
    
    data = {
        "text":question.text,
        "title":question.title,
        "image":question.image,
        "position":question.position,
        "possibleAnswers":[]
    }
    for answer in question.possibleAnswers:
        answerData = {
            "id":answer.id,
            "questionID":answer.questionID,
            "text":answer.text,
            "isCorrect":answer.isCorrect
        }
        data["possibleAnswers"].append(answerData)

    return json.dumps(data)
    


def deserialize(dbJson: json):  
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
        answers.append(answerService.deserialize(question.id, answer))
    question.set_possibleAnswers(answers)

    return question

def insertQuestionRequest(question: Question):
    print("InsertQuestion ",  question.id, question.text, question.title, question.position, question.image)
    if question.id != -1:
        request =  f'INSERT INTO QUESTION(ID, TEXT, TITLE, IMAGE, POSITION) VALUES ("{question.id}","{question.text}", "{question.title}", "{question.image}", {question.position});'
        return request
    else:
        request =  f'INSERT INTO QUESTION(TEXT, TITLE, IMAGE, POSITION) VALUES ("{question.text}", "{question.title}", "{question.image}", {question.position});'
        return request


def getAllQuestions():
    return "SELECT * FROM Question;"

def getQuestionByID(id):
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    request = "SELECT * FROM QUESTION WHERE ID ="+id+";"
    try:
        cursor.execute(request)
        row = cursor.fetchone()
        print(row)
        if(row is not None):
            text = row[1]
            title = row[2]
            image = row[3]
            position = row[4]

            question = Question(id,title,text,image,position)
            question.possibleAnswers=answerService.getAnswersByQuestionID(id)

            return serialize(question), 200
        else:
            return '',401
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        raise err



def createQuestion(question: json):
    print(question)
    #Create new question
    newQuestion = deserialize(question)
    db = connectDB()
    #Use Cursor explicitely, but can be replaced by db.execute() which is a short hand for db.cursor.execute().
    cursor = db.cursor()
    cursor.execute("begin")
    print(insertQuestionRequest(newQuestion))
    #Question Request.
    request = insertQuestionRequest(newQuestion)


    try:
        # save the question to db
        cursor.execute(request)
        print("ID = ", cursor.lastrowid)
        id = cursor.lastrowid
        #Answer Request. TODO : refacto
        for answer in newQuestion.possibleAnswers:
            answer.questionID = id
            aRequest = answerService.insertAnswerRequest(answer)
            cursor.execute(aRequest)

        #send the request
        cursor.execute("commit")
        print("Records created successfully")
        return {'status':'OK'}, 200
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        raise err




