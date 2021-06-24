import config
import requests
import sqlite3
import yfinance
from symbolclass import *
import datetime
import os

def getShareList(index = 2):
    filePath = os.getcwd()
    fileName = filePath + "/" + config.shareList[index]
    with open(fileName, "r", encoding="utf-8") as file:
        shares = file.read()
    shareList = shares.split("\n")
    return shareList

def telegramSend(message):
    botToken = config.telegramBotToken
    botChatId = config.telegramChatId
    message = "<code>" + message + "</code>"
    send_text = 'https://api.telegram.org/bot' + botToken + '/sendMessage?chat_id=' + botChatId + '&parse_mode=Html&text=' + message
    response = requests.get(send_text)
    return response.json()

def createTables():
    filePath = os.getcwd()
    conn = sqlite3.connect(filePath + "/bist.db")
    cursor = conn.cursor()
    query1 = """CREATE TABLE IF NOT EXISTS compare
                (symbol TEXT,
                isPriceFiftyTwoWeekHigh INT,
                isPriceFiftyTwoWeekLow INT,
                isPriceUnderTwoHundredDayAverage INT,
                isPriceUnderFiftyDayAverage INT,
                isPriceUnderBookValue INT,
                isVolumeUnderTenDayAverage INT,
                isVolumeUnderThreeMonth INT,
                isPriceFiveDaysHighest INT,
                isPriceFiveDaysLowest INT,
                isVolumeFiveDaysHighest INT,
                isVolumeFiveDaysLowest INT)
                """
    query2 = """CREATE TABLE IF NOT EXISTS follow
                (symbol TEXT,
                price REAL,
                adDate TEXT,
                fiftyDayAverage REAL,
                twoHundredDayAverage REAL,
                fiftyTwoWeekHigh REAL,
                fiftyTwoWeekLow REAL,
                bookValue REAL,
                removePrice REAL,
                removeDate TEXT,
                profit REAL,
                isClose INT)
                """
    cursor.execute(query1)
    cursor.execute(query2)
    conn.commit()
    conn.close()
    
def compareShareInfo(shareList):
    x = 0
    for i in shareList:
        time = datetime.datetime.now()
        print(f"{time}: {i} hisse senedi bilgileri kontrol ediliyor...")
        try:
            symbol = yfinance.Ticker(i + ".IS")
            message = ""
            share = Share(i, symbol)
            compareList = (
                share.compareTenDayVolume(),
                share.compareThreeMonthVolume(),
                share.comparePriceFiftyDay(),
                share.comparePriceTwoHundredDay(),
                share.checkPriceIfLowest(),
                share.checkPriceIfHighest(),
                share.comparePriceBookValue(),
                share.isFollowable()
            )
            for i in compareList:
                if i != False:
                    message += i
            
            if len(message) > 0:
                message = share.messageHead + message + share.messageEnd
                telegramSend(message)
                print(f"------------\n{message}\n-----------\n")
            else:
                time = datetime.datetime.now()
                print(f"{time}: Değişiklik bulunamadı...")
        except Exception as e:
            print(e)

def getDividend(shareList):
    telegramSend("BU YIL TEMETTÜ DAĞITACAK HİSSELER")
    for i in shareList:
        message = ""
        time = datetime.datetime.now()
        print(f"{time}: {i} hisse senedi temettü bilgileri sorgulanıyor")
        try:
            symbol = yfinance.Ticker(i + ".IS")
            share = Share(i, symbol)
            dividendResult = share.hasDividend()
            if dividendResult != False:
                message += f"{i}: {share.shortName}\n{dividendResult}\n"
                message += f"Hisse Fiyatı: {share.price}\n50 Günlük Ortalama Fiyat: {share.fiftyDayAverage}\nHissenin Yıllık Min - Max Fiyatları: {share.fiftyTwoWeekLow} - {share.fiftyTwoWeekHigh}"
                print(message)
                telegramSend(message)
            
        except Exception as e:
            print(e)


def printFollowList():
    filePath = os.getcwd()
    conn = sqlite3.connect(filePath + "/bist.db")
    cursor = conn.cursor()
    query = "SELECT * FROM follow"
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) > 0:
        cr = " "
        message = "Fiyat  50GOrt 200GOr 52HYük 52HDüş DefDeğ\n"
        for i in result:
            symbol = str(i[0])
            price = str(i[1])
            fiftyDayAverage = str(i[3])
            twoHundredDayAverage = str(i[4])
            fiftyTwoWeekHigh = str(i[5])
            fiftyTwoWeekLow = str(i[6])
            bookValue = str(i[7])
            message += f"{symbol} ----------------\n"
            message += f"{cr*(6-len(price))}{price} {cr*(6-len(fiftyDayAverage))}{fiftyDayAverage} {cr*(6-len(twoHundredDayAverage))}{twoHundredDayAverage}"
            message += f" {cr*(6-len(fiftyTwoWeekHigh))}{fiftyTwoWeekHigh} {cr*(6-len(fiftyTwoWeekLow))}{fiftyTwoWeekLow} {cr*(6-len(bookValue))}{bookValue}\n"
        telegramSend(message)
    
def getFollowedSymbols(status=0):
    filePath = os.getcwd()
    conn = sqlite3.connect(filePath + "/bist.db")
    cursor = conn.cursor()
    query = "SELECT * FROM follow WHERE isClose = ?"
    cursor.execute(query,(status,))
    result = cursor.fetchall()
    chr = " "
    message = ""
    if len(result) > 0:
        if status:
            message += f"HİSSE{2*chr}{2*chr}Alış Tarihi{2*chr}Alış Fiyatı{2*chr}Satış Tarihi{2*chr}Satış Fiyatı{5*chr}Kar\n"
            for i in result:
                symbolName = str(i[0])
                buyPrice = str(i[1])
                buyTime = str(i[2])
                buyDate = buyTime.split("-")[0].replace(" ","")
                selPrice = str(i[8])
                selTime = str(i[9])
                selDate = selTime.split("-")[0].replace(" ","")
                profit = str(i[10])
                message += f"{symbolName}{chr*(7-len(symbolName))}{chr*(13-len(buyDate))}{buyDate}{chr*(13-len(buyPrice))}{buyPrice}{chr*(14-len(selDate))}{selDate}{chr*(14-len(selPrice))}{selPrice}{chr*(8-len(profit))}{profit}\n"
            return message
        else:
            message += f"HİSSE{2*chr}{2*chr}Alış Tarihi{2*chr}Alış Fiyatı\n"
            for i in result:
                symbolName = str(i[0])
                buyPrice = str(i[1])
                buyTime = str(i[2])
                buyDate = buyTime.split("-")[0].replace(" ","")
                profit = str(i[10])
                message += f"{symbolName}{chr*(7-len(symbolName))}{chr*(13-len(buyDate))}{buyDate}{chr*(13-len(buyPrice))}{buyPrice}\n"
            return message
    else:
        return False