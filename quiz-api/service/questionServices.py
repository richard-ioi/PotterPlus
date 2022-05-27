import json
from flask import Flask, request
import model.question as question
import sqlite3

def IsQuestionValid(question):
    if not question['text'] or not question['title'] or not question['position']:
        return False
    return True

def serialize(question : question.Question):
    json.dumps(question.__dict__)

def deserialize(json: str):
    json.loads(json)

def CreateQuestion(question : question.Question):
    #Récupérer le token envoyé en paramètre
    request.headers.get('Authorization')

    #récupèrer un l'objet json envoyé dans le body de la requète
    request.get_json()
    if IsQuestionValid(question):
        serialize(question)

#Génère un objet python  à partir d'une requête sql
def fromSQLResponse(row: tuple):
    return question.Question(row[0], row[1], row[2], row[3], row[4])


