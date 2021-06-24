import sqlite3
import os

class Database:
    def __init__(self, symbol) -> None:
        self.filePath = os.getcwd()
        self.symbol = symbol
        self.con = sqlite3.connect(self.filePath + "/bist.db")
        self.cursor = self.con.cursor()
    
    def writeCompareTable(self):
        query = "INSERT INTO compare VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
        self.cursor.execute(query,(self.symbol,0,0,0,0,0,0,0,0,0,0,0))
        self.con.commit()

    def getSymbolDetail(self):
        query = "SELECT * FROM compare WHERE symbol = ?"
        self.cursor.execute(query, (self.symbol,))
        result = self.cursor.fetchall()
        if len(result) < 1:
            self.writeCompareTable()
            query = "SELECT * FROM compare WHERE symbol = ?"
            self.cursor.execute(query, (self.symbol,))
            result = self.cursor.fetchall()
        return result[0]
    
    def updateCompareTable(self, **kwargs):
        query = "UPDATE compare SET "
        for key, value in kwargs.items():
            query += key + "=" + str(value) + " ,"
        query = query[:-1]
        query += "WHERE symbol = ?"
        self.cursor.execute(query, (self.symbol,))
        self.con.commit()
    
    def getFollowedSymbol(self):
        query = "SELECT * FROM follow WHERE symbol = ? and isClose = 0"
        self.cursor.execute(query, (self.symbol,))
        result = self.cursor.fetchall()
        if len(result) < 1:
            return False
        return result

    def writeFollowTable(self, values):
        query = "INSERT INTO follow VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
        values = tuple(values)
        self.cursor.execute(query, values)
        self.con.commit()
    
    def removeFromFollowed(self, values):
        query = "UPDATE follow SET removePrice = ?, removeDate = ?, profit= ?, isClose = ? WHERE symbol = ?"
        self.cursor.execute(query, (values[0], values[1], values[2], values[3], self.symbol))
        self.con.commit()