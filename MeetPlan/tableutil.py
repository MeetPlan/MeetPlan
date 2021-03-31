from .utils import *
from .models import Meetings, Classes, MeetingGroup
from .emptyobject import EmptyObject
from .objects import MeetingGroupObject

def getOrderedList(classname):
    week = getWeekList(getDate())

    classname = Classes.query.filter_by(name=classname).first()

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
            meeting = Meetings.query.filter_by(date=i, hour=i2, class_id=classname.id).all()
            if meeting:
                if len(meeting) > 1:
                    print(meeting[0].group_id)
                    group = MeetingGroup.query.filter_by(meetingGroup=meeting[0].group_id).first()
                    if index == 0:
                        mon.append(MeetingGroupObject(meeting[0], group.meetingGroup))
                    elif index == 1:
                        tue.append(MeetingGroupObject(meeting[0], group.meetingGroup))
                    elif index == 2:
                        wed.append(MeetingGroupObject(meeting[0], group.meetingGroup))
                    elif index == 3:
                        thu.append(MeetingGroupObject(meeting[0], group.meetingGroup))
                    elif index == 4:
                        fri.append(MeetingGroupObject(meeting[0], group.meetingGroup))
                    elif index == 5:
                        sat.append(MeetingGroupObject(meeting[0], group.meetingGroup))
                else:
                    if index == 0:
                        mon.append(MeetingGroupObject(meeting[0], None))
                    elif index == 1:
                        tue.append(MeetingGroupObject(meeting[0], None))
                    elif index == 2:
                        wed.append(MeetingGroupObject(meeting[0], None))
                    elif index == 3:
                        thu.append(MeetingGroupObject(meeting[0], None))
                    elif index == 4:
                        fri.append(MeetingGroupObject(meeting[0], None))
                    elif index == 5:
                        sat.append(MeetingGroupObject(meeting[0], None))
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

def getOrderedListAPI(classname):
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
                json = {
                    "name": meeting.name,
                    "id": meeting.id,
                    "class": meeting.className,
                    "hour": i2,
                    "weekday": i
                }

                if index == 0:
                    mon.append(json)
                elif index == 1:
                    tue.append(json)
                elif index == 2:
                    wed.append(json)
                elif index == 3:
                    thu.append(json)
                elif index == 4:
                    fri.append(json)
                elif index == 5:
                    sat.append(json)
            else:
                meeting = EmptyObject()
                
                json = {
                    "name": meeting.name,
                    "id": meeting.id,
                    "class": meeting.className,
                    "hour": i2,
                    "weekday": i
                }

                if index == 0:
                    mon.append(json)
                elif index == 1:
                    tue.append(json)
                elif index == 2:
                    wed.append(json)
                elif index == 3:
                    thu.append(json)
                elif index == 4:
                    fri.append(json)
                elif index == 5:
                    sat.append(json)
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
