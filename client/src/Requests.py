def LOGIN(username: str,
          password: str) -> dict:
    return {'type': 'login',
            'username': username,
            'password': password}


def REGISTER(username: str,
             password: str) -> dict:
    return {'type': 'register',
            'username': username,
            'password': password}


def PING() -> dict:
    return {'type': 'ping'}


def LIKE(userID: int,
         articleID: int) -> dict:
    return {'type': 'like',
            'userID': userID,
            'articleID': articleID}


def GET(userID: int,
        articleID: int = 0) -> dict:

    return {'type': 'get',
            'userID': userID,  
            'articleID': articleID}
