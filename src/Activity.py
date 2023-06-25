"""
    This class stores the information for an activity, including the number of guests at it.
    Important fields:
        activityName - name of the activity
        establishmentName - name of the establishment the activity is at
        currActGuests - number of guests at the activity
        maxGuests - max number of guests allowed in the activity
        isOpen - if the activity is open or not (not currently implemented)
"""


class Activity:
    def __init__(self, activityName, establishmentName, currActGuests, isOpen, maxGuests):
        self.activityName = activityName
        self.establishmentName = establishmentName
        self.currentGuests = currActGuests
        self.maxGuests = maxGuests
        self.isOpen = isOpen


    def altStr(self):
        return 'Activity Name: ' + self.activityName + '\n' + \
                'Establishment Name: ' + self.establishmentName + '\n'


    def __str__(self):
        return 'Activity Name: ' + self.activityName + '\n' + \
                'Establishment Name: ' + self.establishmentName + '\n' + \
                'Current Guests: ' + str(self.currentGuests) + '\n'
