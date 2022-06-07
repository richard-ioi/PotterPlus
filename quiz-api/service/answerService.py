from model.answer import Answer
from utils.dbUtils import connectDB


def insertAnswerRequest(answer: Answer):
    """Creates request to insert data into the ANSWER table.

    Parameters
    ----------
    answer : Answer
        The answer that is going to be inserted into the ANSWER table.

    Returns
    -------
    string
        Formatted string, insert request.
    """
    if answer.id != -1:
        request = f'INSERT INTO answer(ID, QUESTION_ID, TEXT, is_Correct) VALUES ({answer.id},{answer.questionID},"{answer.text}", {answer.isCorrect});'
        return request
    else:
        request = f'INSERT INTO answer(QUESTION_ID, TEXT, IS_CORRECT) VALUES ({answer.questionID},"{answer.text}", {answer.isCorrect});'
        return request


def deleteAnswerByQuestionID(questionID):
    """Deletes answer by question ID.

    Parameters
    ----------
    questionID : int
        This id of the question whose answers are going to be cleared.

    Returns
    -------
    tuple
        Http response status.
    """
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    request = f'DELETE FROM ANSWER WHERE QUESTION_ID ="{questionID}";'
    try:
        cursor.execute(request)
        cursor.execute('commit')
        db.close()
        return {'status': 'OK'}, 204
    except Exception as err:
        # in case of exception, roolback the transaction
        cursor.execute('rollback')
        db.close()
        raise err


def getAnswersByQuestionID(questionID):
    """Gets list of answers by question ID.

    Parameters
    ----------
    questionID : int
        This id of the question.

    Returns
    -------
    list
        The answer list related to the question.
    """
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    request = f'SELECT * FROM ANSWER WHERE QUESTION_ID ="{questionID}" ORDER BY ID;'
    answers = []
    try:
        cursor.execute(request)
        rows = cursor.fetchall()
        for row in rows:
            id = row[0]
            text = row[2]
            isCorrect = row[3]
            answers.append(Answer(id, questionID, text, isCorrect))
        db.close()
        return answers
    except Exception as err:
        # in case of exception, roolback the transaction
        cursor.execute('rollback')
        db.close()
        raise err
