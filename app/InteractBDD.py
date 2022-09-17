
try:
	import mariadb
except:
	pass


class PoolOfRequests(object):

	config = {
	    'host': 'mariadb',
	    'port': 3306,
	    'user': 'root',
	    'password': 'pwd',
	    'database': 'data'
	}

	def __init__(self):
		self._conn=mariadb.connect(**PoolOfRequests.config)
		self._cur=self._conn.cursor()
		self._commands=[]

	def __add__(self, command):
		return Request(command.sql, command.commit, self._conn, self._cur).execute()

	
	def __del__(self):
		self._cur.close()
		self._conn.close()


class Request(object):

	def __init__(self, sql, needCommit, conn, cur):
		self._sql=sql
		self._conn=conn
		self._cur=cur
		self._commit=needCommit

	def execute(self):
		if self._commit:
			Request.connectAndExecuteRequest(self._sql, self._commit, self._conn, self._cur)
		else:
			description = Request.connectAndExecuteRequest(self._sql, self._commit, self._conn, self._cur)
			return Resultat(description)
		
	@staticmethod
	def connectAndExecuteRequest(request, needCommit, conn, cur):
		if needCommit:
			try:
				cur.execute(request)
				conn.commit()
			except:
				conn.rollback()
		else:
			cur.execute(request)
		return cur

class Resultat(object):

	def __init__(self, description):
		self._items=[] # c'est une liste de listes
		for item in description:
			self._items.append(list(item))
		self._currentIndex=0

	@property
	def items(self):
		return self._items

	@property
	def singleItems(self):
		items=[]
		for item in self._items:
			items.append(item[0])
		return items

	@property
	def first(self):
		return self._items[0][0]


	def exists(self):
		if isinstance(self.first, int) or isinstance(self.first, str):
			return True
		return False

	def asText(self):
		txt=""
		for item in self._items:
			for elem in item:
				txt= txt+"| " + str(elem)
			txt=txt+"<br>"
		txt=txt+"<br>"
		return txt


class Command(object):

	def __init__(self, sql, needCommit):
		self._sql=sql
		self._commit=needCommit

	@property
	def sql(self):
		return self._sql

	@property
	def commit(self):
		return self._commit





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


