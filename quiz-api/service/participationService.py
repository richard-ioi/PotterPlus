import json
from model.participation import Participation
from model.answerSummary import AnswerSummary
from model.question import Question
import service.questionService as QuestionServices

def createParticipation(participationParameters: json):
    playerName = participationParameters["playerName"]
    answers = participationParameters["answers"]
    if(len(answers)!=QuestionServices.questionCount()):
        raise Exception
    i=0
    score=0
    answerSummaries = []
    for question in QuestionServices.getAllQuestions():
        print(playerName)
        print(i)
        correctAnswerPosition=Question.getCorrectAnswerPosition(question)
        wasCorrect=False
        if(answers[i]==correctAnswerPosition+1):
            wasCorrect=True
            score+=1
        answerSummaries.append(AnswerSummary(correctAnswerPosition,wasCorrect))
        i+=1
    participation = Participation(playerName,score)
    participation.set_AnswerSummaries(answerSummaries)
    return participation