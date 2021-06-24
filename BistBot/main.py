from functions import compareShareInfo, getDividend, printFollowList
import initialize
import datetime
import time

def main():
    printFollow = True
    printDividend = True
    print(initialize.startupMessage)
    while True:
        currentTime = datetime.datetime.now()
        currentDay = datetime.date.today().strftime('%A')
        if ((currentTime.hour == 10 and currentTime.minute > 15) or (currentTime.hour > 10 and currentTime.hour < 18) or (currentTime.hour == 18 and currentTime.minute < 20)) and (currentDay != "Saturday" and currentDay != "Sunday"):
            compareShareInfo(initialize.shareList)
            if currentTime.hour %2 == 0 and currentTime.minute < 10 and printFollow == True:
                printFollowList()
                printFollow = False
            if currentTime.minute > 10:
                printFollow = True
            printDividend = True
        elif currentTime.hour >= 19 and currentTime.hour < 20 and printDividend == True and currentDay != "Saturday" and currentDay != "Sunday":
            getDividend(initialize.shareList)
            printDividend = False
        else:
            print(f"{currentTime} - Endeks Kapalı. 10 dakika sonra tekrar kontrol edilecek...")
            time.sleep(600)

if __name__ == "__main__":
    main()