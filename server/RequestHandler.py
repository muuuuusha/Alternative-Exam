import json
from socketserver import BaseRequestHandler

import Validation

import pickle

RECV_SIZE = 1024*10
ENCODING = 'utf-8'

from DBConnector import SQLiteConnector

OK                   = {'code': ''}
USER_NOT_FOUND       = {'code': 'User not found'}
ARTICLE_NOT_FOUND    = {'code': 'Article not found'}
USER_ALREADY_EXISTS  = {'code': 'User already exists'}
WRONG_PASSWORD       = {'code': 'Wrong password'}
UNKNOWN_REQUEST_TYPE = {'code': 'Unknown request type'}
ALREADY_LIKED        = {'code': 'Already liked'}
NOT_IMPLEMENTED      = {'code': 'Not implemented'}

print('Connecting to database...')
dbConnector = SQLiteConnector()
print('Connected to database')

class RequestHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            data_bytes: bytes = self.request.recv(RECV_SIZE)
            if not data_bytes:
                break

            request: dict = pickle.loads(data_bytes, encoding=ENCODING)

            match request['type']:
                case 'ping':
                    response = OK
                case 'like': 
                    response = self.handleLike(request)
                case 'get': # returns {'code': '', 'articles': [{'id': int, 'title': str, 'text': str, 'likes': int}]}
                    response = self.handleGet(request)
                case 'login': # returns {'code': '', 'data': {'userID': int}}
                    response = self.handleLogin(request)
                case 'register': # returns {'code': '', 'data': {'userID': int}}
                    response = self.handleRegister(request)
                case _:
                    response = UNKNOWN_REQUEST_TYPE
                    print(f'Unknown request type: {request["type"]}')

            self.request.send(pickle.dumps(response))
            
        print(f'Client {self.client_address} disconnected')
    
    
    def handleLike(self, request: dict) -> dict:
        userID    = request['userID']
        articleID = request['articleID']
        
        user = dbConnector.getUser(userID)

        if not user:
            return USER_NOT_FOUND
        if not dbConnector.getArticle(articleID):
            return ARTICLE_NOT_FOUND
        if dbConnector.isLiked(userID, articleID):
            return ALREADY_LIKED

        dbConnector.setLiked(userID, articleID)
        print(f'User {user["username"]} liked article {articleID}')
        
        n = 5
        articles = dbConnector.getRecommendedArticles(user['id'], n)
        
        return {'code': '', 'articles': articles}


    def handleLogin(self, request: dict) -> dict:
        username: str = request['username']
        password: str = request['password']
        
        userID: int = dbConnector.getUserID(username)
        
        if not userID:
            return USER_NOT_FOUND
        
        user: dict = dbConnector.getUser(userID)
        if user['password'] != password:
            return WRONG_PASSWORD

        print(f'User {userID} logged in')
        return {'code': '', 'userID': userID}


    def handleRegister(self, request: dict) -> dict:
        username: str = request['username']
        password: str = request['password']
        
        userID: int = dbConnector.getUserID(username)
        
        if userID:
            return USER_ALREADY_EXISTS

        passwordError: str = Validation.checkPassword(password)
        nicknameError: str = Validation.checkNickname(username)

        if nicknameError:
            return {'code': nicknameError}
        if passwordError:
            return {'code': passwordError}

        userID: int = dbConnector.addUser(username, password)
    

        print(f'User {username} registered')
        return {'code': '', 
                'userID': userID}


    def handleGet(self, request: dict) -> dict:
        isRandom: bool = (request['articleID'] == 0)
        
        if isRandom:
            article = dbConnector.getRandomArticle()
            isLiked = dbConnector.isLiked(request['articleID'], article['id'])
            
            print(f'User {request["userID"]} got article {request["articleID"]}')
            return {'code': '', 
                    'title': article['title'],
                    'content': article['content'], 
                    'articleID': article['id'], 
                    'liked': isLiked }
        else:
            if not dbConnector.getArticle(request['articleID']):
                return {'code': 'Article not found'}
            
            article = dbConnector.getArticle(request['articleID'])
            isLiked = dbConnector.isLiked(request['articleID'], article['id'])
            
            print(f'User {request["userID"]} got article {request["articleID"]}')
            return {'code': '', 
                    'title': article['title'],
                    'articleID': article['id'], 
                    'content': article['content'], 
                    'liked': isLiked }
