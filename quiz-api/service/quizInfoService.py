from utils.dbUtils import connectDB
from model.participation import Participation
from model.participationResult import ParticipationResult
from model.quizInfo import QuizInfo
import service.questionService as QuestionServices

def insertInfoRequest(participation: Participation):
    request =  f'INSERT INTO INFO(PLAYER_NAME, SCORE, DATE) VALUES ("{participation.playerName}", "{participation.score}", strftime("%d/%m/%Y %H:%M:%S",datetime("now")));'
    return request

def getQuizInfo():
    db = connectDB()
    cursor = db.cursor()
    size = QuestionServices.questionCount()
    cursor.execute("begin")
    try:
        cursor.execute("SELECT * FROM INFO ORDER BY SCORE DESC")
        scores=[]
        for row in cursor.fetchall(): 
            playerName=row[0]
            score=row[1]
            date=row[2]
            scores.append(ParticipationResult(playerName,score,date))
        quizInfo = QuizInfo(size)
        quizInfo.set_Scores(scores)
        db.close()
        return QuizInfo.serialize(quizInfo),200
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        db.close()
        raise err

def deleteAllQuizInfo():
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    try:
        cursor.execute("DELETE FROM INFO")
        cursor.execute('commit')
        db.close()
        return '',204
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        db.close()
        raise err


def insertScore(participation):
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    try:
        cursor.execute(insertInfoRequest(participation))
        cursor.execute('commit')
        db.close()
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        db.close()
        raise err