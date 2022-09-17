
from poolOfRequests import PoolOfRequests



class InteractBDD(object):
    
    def __init__(self):
        self._pool=PoolOfRequests()

	 
    @staticmethod
    def getUsername(id):
        return "Beefr"
	 
    @staticmethod
    def getId(username):
        return 1
    
    @staticmethod
    def existInDB(username):
        return True

    
    @staticmethod
    def checkPassword(username, password):
        return True
    
    @staticmethod
    def createUser(username, password):
        return True


