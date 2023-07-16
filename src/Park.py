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
from utils.Schedule import Schedule


class Park:
    def __init__(self):
        # Initialize park variables
        self.activities = []
        self.emptyEstablishments = {}
        self.currentGuests = 0
        self.currentKids = 0
        self.guestsInActivities = 0
        self.activeEstablishments = 0
        self.schedule = Schedule()

    def addActivity(self, act):
        """Add an activity to the activities list, updating any additional fields with it"""
        self.activities.append(act)
        self.guestsInActivities += act.currentGuests
        if act.currentGuests == 0:
            if act.isScheduled:
                self.emptyEstablishments.update({act.establishmentName: act.schedTime})
            else:
                self.emptyEstablishments.update({act.establishmentName: None})


    def finalizeEmptyEstablishments(self):
        """Convert the emptyEstablishments dictionary into an array, to be sorted and displayed"""
        tempArr = []
        for key in self.emptyEstablishments:
            if self.emptyEstablishments.get(key):
                tempArr.append(str(key) + " [Scheduled at " + str(self.emptyEstablishments.get(key)) + "]")
            else:
                tempArr.append(str(key))
        tempArr.sort()
        self.emptyEstablishments = tempArr


    def kidsBusyPercentage(self):
        """Return the percentage of kids currently in activities"""
        if self.currentKids == 0 or self.guestsInActivities == 0:
            return 0
        else:
            return int((self.guestsInActivities / int(self.currentKids)) * 100)
