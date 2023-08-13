"""
    This class stores the information for an activity, including the number of guests at it.
    Important fields:
        activityName - name of the activity
        establishmentName - name of the establishment the activity is at
        currentGuests - number of guests at the activity
        maxGuests - max number of guests allowed in the activity
        isOpen - if the activity is open or not (not currently implemented)
        isScheduled - if the activity is currently scheduled
        schedTime - when the activity is scheduled
"""


class Activity:
    def __init__(self, activityName, establishmentName, currActGuests, isOpen, maxGuests, timeLeft, isScheduled, schedTime):
        self.activityName = activityName
        self.establishmentName = establishmentName
        self.currentGuests = currActGuests
        self.maxGuests = maxGuests
        self.isOpen = isOpen
        self.timeLeft = timeLeft
        self.isScheduled = isScheduled
        self.schedTime = schedTime

    def altStr(self):
        """Return an alternative formatted string of the objected intended to be printed"""
        return 'Activity Name: ' + self.activityName + '\n' + \
            'Establishment Name: ' + self.establishmentName + '\n'

    def __str__(self):
        """Return a formatted string of the object intended to be printed"""
        reply = 'Activity Name: ' + self.activityName + '\n' + \
            'Establishment Name: ' + self.establishmentName + '\n' + \
            'Current Guests: ' + str(self.currentGuests) + '\n' + \
            'Remaining Time: ' + self.timeLeft.__str__() + '\n'
        if self.isScheduled:
            reply += 'Scheduled for: ' + str(self.schedTime) + '\n'
        return reply

