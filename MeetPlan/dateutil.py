from datetime import datetime, timedelta

def getDate():
    day = datetime.now().date()
    return datetime.strptime(str(day), '%Y-%m-%d')

def getStartDate(dt):
    start = dt - timedelta(days=dt.weekday())
    return start

def getStartDateAfter(dt, weeks):
    start = getStartDate(dt)
    print(start)
    start = dt + timedelta(weeks=weeks)
    print(start)
    return start

def getEnd(start):
    end = start + timedelta(days=6)
    return end

def getWeekList(dt):
    start = getStartDate(dt)
    datelist = []
    for i in range(1, 7):
        print(i)
        datelist.append(str(start + timedelta(days=i)).split(" ")[0])
    return datelist
