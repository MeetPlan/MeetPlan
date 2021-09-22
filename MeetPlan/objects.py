from .models import MeetingGroup, Classes

class MeetingGroupObject(object):
    def __init__(self, meeting, groupName, meetings = []):
        self.name = meeting.name
        self.id = meeting.id
        self.className = Classes.query.filter_by(id=meeting.class_id).first().name
        if groupName:
            meetinglist = []
            for meeting in meetings:
                meetinglist.append("- " + meeting.name)
            self.name = groupName + ":<br>" + "<br>".join(meetinglist)
            print(self.name)
            self.isGroup = True
            self.groupName = groupName
        else:
            self.isGroup = False
            self.groupName = groupName