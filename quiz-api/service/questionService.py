import json
from utils.dbUtils import connectDB
from model.question import Question
import service.answerService as answerService


def insertQuestionRequest(question: Question):
    """Creates request to insert data into the QUESTION table.

    Parameters
    ----------
    question : Question
        The question that is going to be inserted into the QUESTION table.

    Returns
    -------
    string
        Formatted string, insert request.
    """
    if question.id != -1:
        request =  f'INSERT INTO QUESTION(ID, TEXT, TITLE, IMAGE, POSITION) VALUES ("{question.id}","{question.text}", "{question.title}", "{question.image}", {question.position});'
        return request
    else:
        request =  f'INSERT INTO QUESTION(TEXT, TITLE, IMAGE, POSITION) VALUES ("{question.text}", "{question.title}", "{question.image}", {question.position});'
        return request

def getAllQuestions():
    """Gets all the question recorded in the QUESTION table.

    Returns
    -------
    list
        List of all database questions.
    """
    db = connectDB()
    cursor = db.cursor()
    questions = []
    cursor.execute("begin")
    try:
        cursor.execute("SELECT * FROM QUESTION ORDER BY POSITION;")
        for row in cursor.fetchall():
            question_id = row[0]
            text = row[1]
            title = row[2]
            image = row[3]
            position = row[4]
            question = Question(question_id,title,text,image,position)
            question.possibleAnswers=answerService.getAnswersByQuestionID(question_id)
            questions.append(question)
        return questions
    except Exception as err:
        #in case of exception, rollback the transaction
        cursor.execute('rollback')
        raise err

def questionCount():
    """Counts the questions in the QUESTION table.

    Returns
    -------
    int
        Number of questions recorded in the QUESTION table.
    """
    db = connectDB()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM QUESTION;")
    total = c.fetchone()[0]
    print("TOTAL : ", total)
    db.close()
    return total

def isPositonTaken(qPosition):
    """ Checks to see if the position of the new question is taken.

    Parameters
    ----------
    qPosition : int
        The position of the new question.

    Returns
    -------
    boolean
        True if the position is taken, False if it is free.

    """
    db = connectDB()
    db.row_factory = lambda cursor, row: row[0]
    c = db.cursor()
    #List that contains all taken positions
    positions = c.execute('SELECT position FROM QUESTION').fetchall()
    print("IDS : ", positions)
    db.close() 

    #Checks if the position if the new question is taken.
    for position in positions:
        if(qPosition == position):
            return True
    return False

def updateQuestionPositions(position):
    """ Updates the value of the existing positions.

    Parameters
    ----------
    position : int
        The position of the new question. All the questions' positons that are greater or equal that position are incremented.
    """
    db = connectDB()
    db.cursor().execute("UPDATE QUESTION SET position = position+1 WHERE position >= ?;",[position])
    db.close()

def createQuestion(newQuestion: Question):
    """Creates the new question in the QUESTION table. 

    The question and related answers are posted to the database.

    Parameters
    ----------
    newQuestion : Question
        The new question.

    Returns
    -------
    tuple
        Http response status.
    """
    db = connectDB()
    #Use of Cursor explicitely, but can be replaced by db.execute() which is a short hand for db.cursor.execute().
    cursor = db.cursor()
    cursor.execute("begin")
    print(insertQuestionRequest(newQuestion))
    #Question Request.
    request = insertQuestionRequest(newQuestion)
    try:
        # save the question to db
        cursor.execute(request)
        id = cursor.lastrowid
        #Answer Request.
        for answer in newQuestion.possibleAnswers:
            answer.questionID = id
            aRequest = answerService.insertAnswerRequest(answer)
            cursor.execute(aRequest)
        #send the request
        cursor.execute("commit")
        print("Records created successfully")
        db.close()
        return {'status':'OK'}, 200
    except Exception as err:
        #in case of exception, rollback the transaction
        cursor.execute('rollback')
        db.close()
        raise err

def deleteQuestionByPosition(position):
    """Deletes question from database by position.

    Parameters
    ----------
    positon : int
        The position of the question to be deleted.

    Returns
    -------
    tuple
        Http response status.
    """
    if(checkIfQuestionExistsByPosition(position)):
        answerService.deleteAnswerByQuestionID(getQuestionIDByPosition(position))
    else:
        return '',404
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    request = f'DELETE FROM QUESTION WHERE POSITION ="{position}";'
    try:
        cursor.execute(request)
        cursor.execute("UPDATE QUESTION SET position = position-1 WHERE position >= ?;",[position])
        cursor.execute('commit')
        db.close()
        return {'status':'OK'}, 204
    except Exception as err:
            #in case of exception, roolback the transaction
            cursor.execute('rollback')
            db.close()
            raise err
            
def getQuestionByPosition(position):
    """Deletes question from database by position.

    Parameters
    ----------
    positon : int
        The position of the question to be deleted.

    Returns
    -------
    tuple
        Http response status.
    """        
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
            return Question.serialize(question), 200
        else:
            return '',404
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        raise err


def updateQuestionByPosition(position: int, question: json):
    """ Updates the question by it's position.

    Parameters
    ----------
    positon : int
        The position of the question to be updated.
    question : json
        The question to be updated.

    Returns
    -------
    tuple
        Http response status.
    """
    newQuestion = Question.deserialize(question)
    if((getQuestionIDByPosition(position)[1])==404):
        return '',404
    question_id=getQuestionIDByPosition(position)[0]
    answerService.deleteAnswerByQuestionID(question_id)
    questionNumber=questionCount()
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    request = f'UPDATE QUESTION SET TEXT="{newQuestion.text}", TITLE="{newQuestion.title}", IMAGE="{newQuestion.image}", POSITION={newQuestion.position} WHERE POSITION ={position};'
    print(request)
    try:
        cursor.execute(request)
        if(position!=newQuestion.position):
            minimum = min(int(position), int(newQuestion.position))
            maximum = max(int(position), int(newQuestion.position))
            #update questions if new position is < questionNumber
            if(newQuestion.position != questionNumber):
                cursor.execute(f'UPDATE QUESTION SET position = position+1 WHERE position >= {minimum} AND position <= {maximum} AND TITLE!="{newQuestion.title}";')
            if(newQuestion.position == questionNumber):
                cursor.execute(f'UPDATE QUESTION SET position = position-1 WHERE position >= {minimum} AND position <= {maximum} AND TITLE !="{newQuestion.title}";')
        for answer in newQuestion.possibleAnswers:
            answer.questionID = question_id
            aRequest = answerService.insertAnswerRequest(answer)
            cursor.execute(aRequest)
        
        cursor.execute('commit')
        db.close()
        return {'status':'OK'}, 200
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        db.close()
        raise err
        
def checkQuestionPosition(question: json):
    """Checks the positon of the new question before posting it to database. 

    The position of the new question is checked, and the existing positions are updated if necessary.
    The new question is created.

    Parameters
    ----------
    question : json
        The new question.

    Returns
    -------
    tuple
        Http response status.
    """
    newQuestion = Question.deserialize(question)
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
    """Checks to see if a question exists at the position parameter.

    Parameters
    ----------
    positon : int
        The position of the question.

    Returns
    -------
    boolean
        True if the question at the position exists. Else false.
    """
    if(getQuestionByPosition(position)[1]==404):
        return False
    else:
        return True

def getQuestionIDByPosition(position):
    """Gets question ID by position.

    Parameters
    ----------
    positon : int
        The position of the question.

    Returns
    -------
    tuple
        The question ID and the Http response status.
    """
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    request=f'SELECT ID FROM QUESTION WHERE POSITION="{position}";'
    try:
        cursor.execute(request)
        row = cursor.fetchone()
        db.close()
        if(row is not None):
            question_id = row[0]
            return question_id, 200
        else:
            return '',404
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        db.close()
        raise err