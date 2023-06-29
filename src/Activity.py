"""
    This class stores the information for an activity, including the number of guests at it.
    Important fields:
        activityName - name of the activity
        establishmentName - name of the establishment the activity is at
        currActGuests - number of guests at the activity
        maxGuests - max number of guests allowed in the activity
        isOpen - if the activity is open or not (not currently implemented)
"""

import src.utils.EndTime


class Activity:
    def __init__(self, activityName, establishmentName, currActGuests, isOpen, maxGuests, timeLeft):
        self.activityName = activityName
        self.establishmentName = establishmentName
        self.currentGuests = currActGuests
        self.maxGuests = maxGuests
        self.isOpen = isOpen
        self.timeLeft = timeLeft

    def altStr(self):
        """Return an alternative formatted string of the objected intended to be printed"""
        return 'Activity Name: ' + self.activityName + '\n' + \
            'Establishment Name: ' + self.establishmentName + '\n'

    def __str__(self):
        """Return a formatted string of the object intended to be printed"""
        return 'Activity Name: ' + self.activityName + '\n' + \
            'Establishment Name: ' + self.establishmentName + '\n' + \
            'Current Guests: ' + str(self.currentGuests) + '\n' + \
            'Remaining Time: ' + self.timeLeft.__str__() + '\n'
