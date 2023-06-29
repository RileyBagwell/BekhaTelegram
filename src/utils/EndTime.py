"""
    Contains the data for an activity's end time
"""

class EndTime:
    def __init__(self, str):
        """Create a Time object given a TimeEnd field from the API"""
        self.minutes = str[:2]
        self.seconds = str[3:]

    def __str__(self):
        return f"{self.minutes}:{self.seconds}"

    def timeLeft(self):
        """Return the time left in english"""
        return f"{self.minutes} minutes and {self.seconds} seconds"
