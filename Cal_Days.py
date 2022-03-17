import datetime


def AddDays(sourceDate, count): #특정요일의 마지막주를 찾기위한 함수
    targetDate = sourceDate + datetime.timedelta(days = count + 1) 
    #print("targetDate: ",targetDate)
    return targetDate

def GetWeekLastDate(): #특정요일의 마지막주를 찾기위한 함수 2
    now = datetime.datetime.now() #현재 날짜
    now = now.date() #현재 날짜
    temporaryDate = datetime.datetime(now.year, now.month, now.day) 
    weekDayCount = temporaryDate.weekday() 
    targetDate = AddDays(now, -weekDayCount + 8); 
    return targetDate