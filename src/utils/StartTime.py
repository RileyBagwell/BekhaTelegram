"""
    Manages StartDateTime from the SQL database
    UNUSED
"""
from datetime import datetime


class StartDateTime:
    def __init__(self, str):
        """Create a Time object given a StartDateTime field from the database.
            format is 'yyyy-mm-dd hh:mm:ss.sss'"""
        index = str.index(' ')
        self.hour = str[index + 1:index + 3]
        self.minute = str[index + 4:index + 6]
        self.second = str[index + 7:index + 9]
        self.period = ''
        self.adjustMilitary()  # Convert out of military time


    def __str__(self):
        return f"{int(self.hour)}:{self.minute}:{self.second} {self.period}"


    def adjustMilitary(self):
        """Adjust the time from military time"""
        if int(self.hour) >= 12:
            self.period = 'PM'
            if self.hour != 12:
                self.hour = str(int(self.hour) - 12)
        else:
            self.period = 'AM'


    def isInFuture(self):
        """Return true if this time is in the future.
            Unfinished and unused."""
        time = datetime.now()  # Used for the timestamp
        currTime = time.strftime("%H:%M:%S") + ' ' + str(time.date())
