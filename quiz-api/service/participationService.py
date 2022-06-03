import json
from model.participation import Participation
from model.answerSummary import AnswerSummary
from service.questionServices import QuestionServices
from utils.dbUtils import connectDB

def insertInfoRequest(participation: Participation):
    if participation.id != -1:
        request =  f'INSERT INTO INFO(ID, PLAYER_NAME, SCORE, DATE) VALUES ("{participation.id}","{participation.playerName}", "{participation.score}", SYSDATE);'
        return request
    else:
        request =  f'INSERT INTO INFO(PLAYER_NAME, SCORE, DATE) VALUES ("{participation.playerName}", "{participation.score}", SYSDATE);'
        return request

def getQuizInfo():
    db = connectDB()
    c = db.cursor()
    c.execute("SELECT * FROM INFO ORDER BY SCORE")
    c.fetchall()

def saveParticipation(participationParameters: json):
    playerName = participationParameters["player_name"]
    answers = participationParameters["answers"]
    i=0
    score=0
    answerSummaries = []
    for question in QuestionServices.getAllQuestions():
        correctAnswerPosition=QuestionServices.getCorrectAnswerPosition(question)
        wasCorrect=False
        if(answers[i]==correctAnswerPosition):
            wasCorrect=True
            score+=1
        answerSummaries.append(AnswerSummary(correctAnswerPosition,wasCorrect))
    participation = Participation(playerName,score)
    participation.set_AnswerSummaries(answerSummaries)
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("begin")
    try:
        cursor.execute(insertInfoRequest(participation))
        cursor.execute('commit')
        return serialize(participation),200
    except Exception as err:
        #in case of exception, roolback the transaction
        cursor.execute('rollback')
        raise err