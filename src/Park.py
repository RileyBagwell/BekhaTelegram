"""
    Manages all the establishments in the park with their activities
    Important fields:
        activities - list of Activity objects
        emptyEstablishments - dictionary of activities with kids in them
        currentGuests - # of guests in the park
        currentKids - # of kids in the park
        guestsInActivities - # of kids in all activities
        activeEstablishments - # of establishments with kids in them
"""

import Activity


class Park:
    def __init__(self):
        # Initialize park variables
        self.activities = []
        self.emptyEstablishments = {}
        self.currentGuests = 0
        self.currentKids = 0
        self.guestsInActivities = 0
        self.activeEstablishments = 0

    def addActivity(self, act):
        """Add an activity to the activities list, updating any additional fields with it"""
        self.activities.append(act)
        self.guestsInActivities += act.currentGuests
        if act.currentGuests > 0:
            self.emptyEstablishments.update({act.establishmentName: 1})


    def kidsBusyPercentage(self):
        """Return the percentage of kids currently in activities"""
        if self.currentKids == 0 or self.guestsInActivities == 0:
            return 0
        else:
            return int((self.guestsInActivities / int(self.currentKids)) * 100)
