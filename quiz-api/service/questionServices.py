import json
from venv import create
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
        "position":int(question.position),
        "possibleAnswers":[]
    }
    for answer in question.possibleAnswers:
        isCorrect=True
        if(answer.isCorrect==0):
            isCorrect=False
        answerData = {
            "id":answer.id,
            "questionID":answer.questionID,
            "text":answer.text,
            "isCorrect":isCorrect
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
    if question.id != -1:
        request =  f'INSERT INTO QUESTION(ID, TEXT, TITLE, IMAGE, POSITION) VALUES ("{question.id}","{question.text}", "{question.title}", "{question.image}", {question.position});'
        return request
    else:
        request =  f'INSERT INTO QUESTION(TEXT, TITLE, IMAGE, POSITION) VALUES ("{question.text}", "{question.title}", "{question.image}", {question.position});'
        return request

#Get all questions.
def getAllQuestions():
    db = connectDB()
    c = db.cursor()
    c.execute("SELECT json_group_array( json_object('ID', id, 'TEXT', text,'TITLE', title, 'IMAGE', image, 'POSITION', position)) FROM QUESTION;")
    questionsList = c.fetchall()
    print("QUESTIONLIST", questionsList)
    db.close()
    questions = []
    for question in questionsList:
        print(question)
        # question = json.dumps(question)
        # print("question in for", json.loads(question))
        # questions.append(deserialize(json.loads(question)))
    print("DESERIALIZED QUESTIONS", questions)
    return questionsList

#Count all questions.
def questionCount():
    db = connectDB()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM QUESTION;")
    total = c.fetchone()[0]
    print("TOTAL : ", total)
    db.close()
    return total

#Checks to see if the position of the new question is taken.
def isPositonTaken(qPosition):
    db = connectDB()
    db.row_factory = lambda cursor, row: row[0]
    c = db.cursor()
    #List that contains all taken positions
    positions = c.execute('SELECT position FROM QUESTION').fetchall()
    print("IDS : ", positions)
    db.close() 

    #Verifier que la position de la nouvelle question est différente de celles existantes
    for position in positions:
        if(qPosition == position):
            return True
    return False

#Updates the value of of the existing positions.
def updateQuestionPositions(position):
    db = connectDB()
    db.cursor().execute("UPDATE QUESTION SET position = position+1 WHERE position >= ?;",[position])
    db.close()

def createQuestion(newQuestion: Question):
    #Create new question
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
        #in case of exception, rollback the transaction
        cursor.execute('rollback')
        raise err

def deleteQuestionByPosition(position):
    if(checkIfQuestionExistsByPosition(position)):
        answerService.deleteAnswerByQuestionID(id)
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    request = f'DELETE FROM QUESTION WHERE POSITION ="{position}";'
    try:
        cursor.execute(request)
        if(checkIfQuestionExistsByPosition(position)):
            return {'status':'OK'}, 204
        else:
            return '',404
    except Exception as err:
            #in case of exception, roolback the transaction
            cursor.execute('rollback')
            raise err
            
def getQuestionByPosition(position):
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    request = f'SELECT * FROM QUESTION WHERE POSITION ="{position}";'
    try:
        cursor.execute(request)
        row = cursor.fetchone()
        if(row is not None):
            question_id = row[0]
            text = row[1]
            title = row[2]
            image = row[3]

            question = Question(question_id,title,text,image,position)
            question.possibleAnswers=answerService.getAnswersByQuestionID(question_id)
            return serialize(question), 200
        else:
            return '',404
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        raise err

def updateQuestionByPosition(position, question: json):
    newQuestion = deserialize(question)
    if((getQuestionIDByPosition(position)[1])==404):
        return '',404
    question_id=getQuestionIDByPosition(position)[0]
    answerService.deleteAnswerByQuestionID(question_id)
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    request = f'UPDATE QUESTION SET TEXT="{newQuestion.text}", TITLE="{newQuestion.title}", IMAGE="{newQuestion.image}", POSITION={newQuestion.position} WHERE POSITION ={position};'
    print(request)
    try:
        cursor.execute(request)
        cursor.execute('commit')
        if(checkIfQuestionExistsByPosition(newQuestion.position)):
            for answer in newQuestion.possibleAnswers:
                answer.questionID = question_id
                aRequest = answerService.insertAnswerRequest(answer)
                cursor.execute(aRequest)
            return {'status':'OK'}, 200
        else:
            return '',404
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        raise err
        
def checkQuestionPosition(question: json):
    newQuestion = deserialize(question)
    if(newQuestion.position > questionCount()+1 or newQuestion.position < 0):
        return {"status":"KO"}, 400
    if isPositonTaken(newQuestion.position):
        updateQuestionPositions(newQuestion.position)
        createQuestion(newQuestion)
        return {'status':'OK'}, 200
    else:
        createQuestion(newQuestion)
        return {'status':'OK'}, 200

def checkIfQuestionExistsByPosition(position):
    if(getQuestionByPosition(position)[1]==404):
        return False
    else:
        return True

def getQuestionIDByPosition(position):
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    request=f'SELECT ID FROM QUESTION WHERE POSITION="{position}";'
    try:
        cursor.execute(request)
        row = cursor.fetchone()
        if(row is not None):
            question_id = row[0]
            return question_id, 200
        else:
            return '',404
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        raise err
