from .models import MeetingGroup, Classes

class MeetingGroupObject(object):
    def __init__(self, meeting, groupName):
        self.name = meeting.name
        self.id = meeting.id
        self.className = Classes.query.filter_by(id=meeting.class_id).first().name
        if groupName:
            self.name = groupName
            self.isGroup = True
            self.groupName = groupName
        else:
            self.isGroup = False
            self.groupName = groupName