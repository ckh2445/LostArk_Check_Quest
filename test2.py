import datetime
import Cal_Days

now = datetime.datetime.now()
#now = str(now.strftime('%Y-%m-%d %H:%M:%S'))
#now2 = datetime.datetime(now)
#today6am = now.replace(hour=6, minute=0, second=0, microsecond=0)
#now2 = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

#print(now2)
#print(today6am)

next_day = now + datetime.timedelta(days=1) #다음날 날짜
next_day = next_day.replace(hour=6, minute=0, second=0, microsecond=0) #시간정리
#Characters_info["next_day"] = str(next_day.strftime("%Y-%m-%d %H:%M:%S"))
next_week = str(Cal_Days.GetWeekLastDate())
next_week = datetime.datetime.strptime(next_week, '%Y-%m-%d')
next_week = next_week.replace(hour=6, minute=0, second=0, microsecond=0)
print((now - next_day).days)
print(next_day)
#next_week = next_week.replace(hour=6, minute=0, second=0, microsecond=0) #시간정리
#Characters_info["next_week"] = str(next_week)