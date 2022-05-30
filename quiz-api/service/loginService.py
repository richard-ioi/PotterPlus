from flask import Flask, request
from utils.jwt_utils import build_token

def isPasswordCorrect():
    payload = request.get_json()
    if payload['password'] == 'Vive l\'ESIEE !':
        return {'token': build_token()}
    else : 
        return '', 401

