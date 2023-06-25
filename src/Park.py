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
        self.activities.append(act)
        self.guestsInActivities += act.currentGuests
        if act.currentGuests > 0:
            self.emptyEstablishments.update({act.establishmentName: 1})
