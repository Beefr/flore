
try:
	import mariadb
except:
	pass


class InteractBDD(object):
    
    config = {
	    'host': 'mariadb-anog-service',
	    'port': 3306,
	    'user': 'root',
	    'password': 'pwd',
	    'database': 'data'
	}
    
    
    @staticmethod
    def getUsername(id):
        return None
    
    @staticmethod
    def existInDB(username):
        return None

    
    @staticmethod
    def checkPassword(username, password):
        return None
    
    @staticmethod
    def createUser(username, password):
        return None


    #____________________________________________________________
    
    @staticmethod
    def connectAndExecuteRequest(request, needCommit, conn, cur):
        #conn = mariadb.connect(**InteractBDD.config)
        #cur = conn.cursor()
        if needCommit:
            try:
                cur.execute(request)
                conn.commit()
            except:
                conn.rollback()
        else:
            cur.execute(request)

        description=cur
        #cur.close()
        #conn.close()
        return description

    @staticmethod
    def beginQuery():
        conn = mariadb.connect(**InteractBDD.config)
        cur = conn.cursor()
        return [conn, cur]

    @staticmethod
    def endQuery(conn, cur):
        cur.close()
        conn.close()

