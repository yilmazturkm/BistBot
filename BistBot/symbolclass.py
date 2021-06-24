from databaseclass import *
import datetime


class Share:
    def __init__(self, symbol, symbolDetail) -> None:
        self.symbol = symbol
        self.symbolInfo = symbolDetail.info
        self.symbolHistory = symbolDetail.history(period="6d")
        self.shortName = self.symbolInfo["shortName"]
        self.price = self.symbolInfo["regularMarketPrice"]
        self.dayLow = self.symbolInfo["dayLow"]
        self.dayHigh = self.symbolInfo["dayHigh"]
        self.fiftyDayAverage = round(self.symbolInfo["fiftyDayAverage"], 2)
        self.twoHundredDayAverage = round(self.symbolInfo["twoHundredDayAverage"], 2)
        self.previousClose = self.symbolInfo["previousClose"]
        self.volume = self.symbolInfo["regularMarketVolume"]
        self.tenDayVolume = self.symbolInfo["averageVolume10days"]
        self.threeMonthVolume = self.symbolInfo["averageVolume"]
        self.fiftyTwoWeekLow = round(self.symbolInfo["fiftyTwoWeekLow"], 2)
        self.fiftyTwoWeekHigh = round(self.symbolInfo["fiftyTwoWeekHigh"], 2)
        self.bookValue = round(self.symbolInfo["bookValue"], 2)
        self.messageHead = f"{self.symbol}: {self.shortName}\n"
        self.messageEnd = f"Fiyat: {self.price}\nGünlük En Düşük: {self.dayLow}\nGünlük En Yüksek: {self.dayHigh}\nÖnceki Gün Kapanış: {self.previousClose}\n50 Günlük Ortalama: {self.fiftyDayAverage}\n200 Günlük Ortalama: {self.twoHundredDayAverage}\n52 Haftanın En Düşük Fiyatı: {self.fiftyTwoWeekLow}\n52 Haftanın En Yüksek Fiyatı: {self.fiftyTwoWeekHigh}\nDefter Değeri: {self.bookValue}\nHacim: {self.volume}\nOn Günlük Hacim: {self.tenDayVolume}\nÜç Aylık Hacim: {self.threeMonthVolume}"
        self.database = Database(self.symbol)
        self.compareSymbol = self.database.getSymbolDetail()
        self.nowTime = datetime.datetime.now()

    def compareTenDayVolume(self): # Mevcut hacmi 10 günlük ortalama hacimle karşılaştır
        if self.volume < self.tenDayVolume and self.compareSymbol[6] == 0: # Hacim 10 günlük hacimden küçükse ve veritabanında daha önce büyük olduğu kaydedilmişse
            self.database.updateCompareTable(isVolumeUnderTenDayAverage = 1)
            if self.nowTime.hour > 11:
                return "- Hacim 10 günlük ortalama hacmin altına düştü\n" # Hacmin düştü
            return False
        elif self.volume > self.tenDayVolume and self.compareSymbol[6] == 1: # Hacim 10 günlük hacimden büyükse ve veritabanında daha önce küçük olduğu kaydedilmişse
            self.database.updateCompareTable(isVolumeUnderTenDayAverage = 0)
            return "- Hacim 10 günlük ortalama hacmin üstüne çıktı\n" # Hacim çıktı
        return False # Eğer hiç bir koşula uymuyorsa False döndür
    
    def compareThreeMonthVolume(self):
        if self.volume < self.threeMonthVolume and self.compareSymbol[7] == 0:
            self.database.updateCompareTable(isVolumeUnderThreeMonth = 1)
            if self.nowTime.hour > 11:
                return "- Hacim 3 aylık ortalama hacmin altına düştü\n"
            return False
        elif self.volume > self.threeMonthVolume and self.compareSymbol[7] == 1:
            self.database.updateCompareTable(isVolumeUnderThreeMonth = 0)
            return "- Hacim 3 aylık ortalama hacmin üstüne çıktı\n"
        return False
    
    def comparePriceFiftyDay(self):
        if self.price < self.fiftyDayAverage * 0.95 and self.compareSymbol[4] == 0:
            self.database.updateCompareTable(isPriceUnderFiftyDayAverage = 1)
            return "- Fiyat 50 günlük ortalama fiyatın %5 altına düştü\n"
        elif self.price > self.fiftyDayAverage * 1.05 and self.compareSymbol[4] == 1:
            self.database.updateCompareTable(isPriceUnderFiftyDayAverage = 0)
            return "- Fiyat 50 günlük ortalama fiyatın %5 üstüne çıktı\n"
        return False

    def comparePriceTwoHundredDay(self):
        if self.price < self.twoHundredDayAverage * 0.95 and self.compareSymbol[3] == 0:
            self.database.updateCompareTable(isPriceUnderTwoHundredDayAverage = 1)
            return "- Fiyat 200 günlük ortalama fiyatın %5 altına düştü\n"
        elif self.price > self.twoHundredDayAverage * 1.05 and self.compareSymbol[3] == 1:
            self.database.updateCompareTable(isPriceUnderTwoHundredDayAverage = 0)
            return "- Fiyat 200 günlük ortalama fiyatın %5 üstüne çıktı\n"
        return False
    
    def checkPriceIfLowest(self):
        if self.price <= self.fiftyTwoWeekLow and self.compareSymbol[2] == 0:
            self.database.updateCompareTable(isPriceFiftyTwoWeekLow = 1)
            return "- Fiyat 52 haftanın en düşük fiyatı\n"
        elif self.price > self.fiftyTwoWeekLow and self.compareSymbol[2] == 1:
            self.database.updateCompareTable(isPriceFiftyTwoWeekLow = 0)
            return "- Fiyat 52 haftanın en düşük fiyatının üzerine çıktı\n"
        return False
    
    def checkPriceIfHighest(self):
        if self.price >= self.fiftyTwoWeekHigh and self.compareSymbol[1] == 0:
            self.database.updateCompareTable(isPriceFiftyTwoWeekHigh = 1)
            return "- Fiyat 52 haftanın en yüksek fiyatı\n"
        elif self.price < self.fiftyTwoWeekHigh and self.compareSymbol[1] == 1:
            self.database.updateCompareTable(isPriceFiftyTwoWeekHigh = 0)
            return "- Fiyat 52 haftanın en yüksek fiyatının altına düştü\n"
        return False
    
    def comparePriceBookValue(self):
        if self.price < self.bookValue * 0.95 and self.compareSymbol[5] == 0:
            self.database.updateCompareTable(isPriceUnderBookValue = 1)
            return "- Fiyat defter değerinin %5 altına düştü\n"
        elif self.price > self.bookValue * 1.05 and self.compareSymbol[5] == 1:
            self.database.updateCompareTable(isPriceUnderBookValue = 0)
            return "- Fiyat defter değerinin %5 üstüne çıktı\n"
        return False

    def isFollowable(self):
        followedSymbols = self.database.getFollowedSymbol()
        if (self.price < self.bookValue * 0.95 and self.price < self.fiftyDayAverage * 0.95 and self.price < self.twoHundredDayAverage * 0.95) or (self.price < self.fiftyDayAverage and self.volume > self.tenDayVolume and self.volume > self.threeMonthVolume):
            if followedSymbols == False:
                adDate = self.nowTime.strftime("%d.%m.%Y - %H:%M")
                self.database.writeFollowTable(
                    [self.symbol,
                    self.price,
                    adDate,
                    self.fiftyDayAverage,
                    self.twoHundredDayAverage,
                    self.fiftyTwoWeekHigh,
                    self.fiftyTwoWeekLow,
                    self.bookValue,
                    None,
                    None,
                    None,
                    0]
                    )
                return "- Takip listesine eklendi\n"
            return False
        elif (self.price > self.bookValue * 1.05 and self.price > self.fiftyDayAverage * 1.05 and self.price * 1.05 and self.price > self.twoHundredDayAverage *1.05) or (self.price > self.fiftyDayAverage * 1.05 and self.volume > self.tenDayVolume and self.volume > self.threeMonthVolume):
            if followedSymbols != False:
                addPrice = followedSymbols[0][1]
                removeDate = self.nowTime.strftime("%d.%m.%Y - %H:%M")
                profit = round(((self.price - addPrice)*100)/addPrice, 2)
                self.database.removeFromFollowed(
                    [self.price,
                    removeDate,
                    profit,
                    1]
                )
                return "- Takip listesinden çıkartıldı\n"
            return False
        else:
            return False
    
    def isLastFiveDaysHighestPrice(self):
        if self.price > self.lastFiveDaysHighestPrice and self.compareSymbol[8] == 0:
            self.database.updateCompareTable(isPriceFiveDaysHighest = 1)
            return "- Son 5 günün en yüksek fiyatı!"
        elif self.price < self.lastFiveDaysHighestPrice and self.compareSymbol[8] == 1:
            self.database.updateCompareTable(isPriceFiveDaysHighest = 0)
            return False
        return False
    
    def isLastFiveDaysLowestPrice(self):
        if self.price < self.lastFiveDaysLowestPrice and self.compareSymbol[9] == 0:
            self.database.updateCompareTable(isPriceFiveDaysLowest = 1)
            return "- Son 5 günün en düşük fiyatı"
        elif self.price > self.lastFiveDaysLowestPrice and self.compareSymbol[9] == 1:
            self.database.updateCompareTable(isPriceFiveDaysLowest = 0)
            return False
        return False
    
    def isLastFiveDayHighestVolume(self):
        if self.volume > self.lastFiveDaysHighestVolume and self.compareSymbol[10] == 0:
            self.database.updateCompareTable(isVolumeFiveDaysHighest = 1)
            return "- Son 5 günün en yüksek hacmi"
        elif self.volume < self.lastFiveDaysHighestVolume and self.compareSymbol[10] == 1:
            self.database.updateCompareTable(isVolumeFiveDaysHighest = 0)
            return False
        return False
    
    def isLastFiveDayLowestVolume(self):
        if self.volume < self.lastFiveDaysLowestVolume and self.compareSymbol[11] == 0:
            self.database.updateCompareTable(isVolumeFiveDaysLowest = 1)
            return "- Son 5 günün en düşük hacmi"
        elif self.volume > self.lastFiveDaysLowestVolume and self.compareSymbol[11] == 1:
            self.database.updateCompareTable(isVolumeFiveDaysLowest = 0)
            return False
        return False

    def hasDividend(self):
        message = ""
        exDividendDate = self.symbolInfo["exDividendDate"]
        trailingAnnualDividendRate = self.symbolInfo["trailingAnnualDividendRate"]
        trailingAnnualDividendYield = self.symbolInfo["trailingAnnualDividendYield"]
        if exDividendDate != None:
            exDividendDate = datetime.datetime.fromtimestamp(exDividendDate)
            if exDividendDate.year == self.nowTime.year and exDividendDate.month >= self.nowTime.month:
                exDividendDate = exDividendDate.strftime("%d-%m-%Y")
                message += f"Temettü Tarihi: {exDividendDate}\n"
                if trailingAnnualDividendRate != None:
                    message += f"Temettü Değeri: {trailingAnnualDividendRate}\n"
                if trailingAnnualDividendYield != None:
                    message += f"Temettü Verimi: {trailingAnnualDividendYield}\n"
                return message
            return False
        return False