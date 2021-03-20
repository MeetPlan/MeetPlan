from .utils import *
from .models import Meetings
from .emptyobject import EmptyObject

def getOrderedList(classname):
    week = getWeekList(getDate())

    mon = []
    tue = []
    wed = []
    thu = []
    fri = []
    sat = []

    index = 0
    for i in week:
        for i2 in range(9):
            #print(i2)
            meeting = Meetings.query.filter_by(date=i, hour=i2, className=classname).first()
            if meeting:
                if index == 0:
                    mon.append(meeting)
                elif index == 1:
                    tue.append(meeting)
                elif index == 2:
                    wed.append(meeting)
                elif index == 3:
                    thu.append(meeting)
                elif index == 4:
                    fri.append(meeting)
                elif index == 5:
                    sat.append(meeting)
            else:
                if index == 0:
                    mon.append(EmptyObject())
                elif index == 1:
                    tue.append(EmptyObject())
                elif index == 2:
                    wed.append(EmptyObject())
                elif index == 3:
                    thu.append(EmptyObject())
                elif index == 4:
                    fri.append(EmptyObject())
                elif index == 5:
                    sat.append(EmptyObject())
        index += 1
    
    json = {
        "mon": mon,
        "tue": tue,
        "wed": wed,
        "thu": thu,
        "fri": fri,
        "sat": sat
    }

    #print(json)
    
    return json
