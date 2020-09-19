class db():
    def __init__(self, storage):
        self.checkpath()
        self.storage = storage
        storage.database = self
        import cx_Oracle
        self.connect = cx_Oracle.connect(self.storage.dbconfig["user"], self.storage.dbconfig["passwd"], self.storage.dbconfig["dbname"], encoding="UTF-8")

        try:
            pass
        except:
            print("Something Went Wrong!")
            exit()
        self.get = get(storage)
        self.cursor = cursor(storage)
        self.mcursor = self.cursor.create()

    def checkpath(self):
        from os import environ
        try:
            tmp = environ["ORACLE_HOME"]
        except:
            print("Cannot find ORACLE_HOME")
            exit()
        try:
            tmp = environ["TNS_ADMIN"]
        except:
            print("Cannot find TNS_ADMIN")
            exit()
        if environ["ORACLE_HOME"] in environ["PATH"]: pass
        else: 
            print("Cannot find ORACLE_HOME in path")
            exit()
            

    def __end__(self):
        del self.get
        del self.cursor
        self.connect.close()
        self.storage.database = None

    def commit(self): self.connect.commit()
    def close(self): del self

class cursor():
    def __init__(self, storage):
        self.storage = storage
        self.connect = storage.database.connect
        pass

    def refreshcursor(self, cursor):
        self.delete(cursor)
        return self.create()

    def create(self): return self.connect.cursor()
    def delete(self, cursor): cursor.close()

class get():
    def __init__(self, storage):
        self.storage = storage
        self.connect = storage.database.connect

    def chkwork(self):
        sql = "SELECT A.LOGIN, B.REGION, C.WORK, C.BROADCASTING, C.NOWTIMEFROM tdb.STREAMERSTATUSLOG a , tdb.STREAMERS b, (SELECT ID, WORK, BROADCASTING, NOWTIMEFROM (SELECT ID, WORK, BROADCASTING, NOWTIME, (ROW_NUMBER() OVER(PARTITION BY ID ORDER BY NOWTIME DESC)) RANKFROM TDB.STATUSWHERE NOWTIME > sysdate - 30)WHERE RANK = 1) c WHERE A.LOGIN = B.LOGIN and C.ID = A.ID and REGION=:1 and C.WORK = 'IDLE', C.BROADCASTING = 1"
        self.storage.database.mcursor.execute(sql,shin08070919
        )


#SELECT A.LOGIN, B.REGION, C.WORK, C.BROADCASTING, C.NOWTIMEFROM tdb.STREAMERSTATUSLOG a , tdb.STREAMERS b, (SELECT ID, WORK, BROADCASTING, NOWTIMEFROM (SELECT ID, WORK, BROADCASTING, NOWTIME, (ROW_NUMBER() OVER(PARTITION BY ID ORDER BY NOWTIME DESC)) RANKFROM TDB.STATUSWHERE NOWTIME > sysdate - 30)WHERE RANK = 1) c WHERE A.LOGIN = B.LOGIN and C.ID = A.ID and REGION=:1;
#SELECT A.LOGIN, B.REGION, C.WORK, C.BROADCASTING, C.NOWTIMEFROM tdb.STREAMERSTATUSLOG a , tdb.STREAMERS b, (SELECT ID, WORK, BROADCASTING, NOWTIMEFROM (SELECT ID, WORK, BROADCASTING, NOWTIME, (ROW_NUMBER() OVER(PARTITION BY ID ORDER BY NOWTIME DESC)) RANKFROM TDB.STATUSWHERE NOWTIME > sysdate - 30)WHERE RANK = 1) c WHERE A.LOGIN = B.LOGIN and C.ID = A.ID and REGION=:1 and C.WORK = "IDLE", C.BROADCASTING = 1;
#SELECT A.LOGIN, B.REGION, C.WORK, C.BROADCASTING, C.NOWTIMEFROM tdb.STREAMERSTATUSLOG a , tdb.STREAMERS b, (SELECT ID, WORK, BROADCASTING, NOWTIMEFROM (SELECT ID, WORK, BROADCASTING, NOWTIME, (ROW_NUMBER() OVER(PARTITION BY ID ORDER BY NOWTIME DESC)) RANKFROM TDB.STATUSWHERE NOWTIME > sysdate - 30)WHERE RANK = 1) c WHERE A.LOGIN = B.LOGIN and C.ID = A.ID and REGION=:1 and C.WORK = :2, C.BROADCASTING = :3;
#SELECT A.LOGIN, B.REGION, C.WORK, C.BROADCASTING, C.NOWTIMEFROM tdb.STREAMERSTATUSLOG a , tdb.STREAMERS b, (SELECT ID, WORK, BROADCASTING, NOWTIMEFROM (SELECT ID, WORK, BROADCASTING, NOWTIME, (ROW_NUMBER() OVER(PARTITION BY ID ORDER BY NOWTIME DESC)) RANKFROM TDB.STATUSWHERE NOWTIME > sysdate - 30)WHERE RANK = 1) c WHERE A.LOGIN = B.LOGIN and C.ID = A.ID and REGION=:1 and C.WORK = :2, C.BROADCASTING = :3;