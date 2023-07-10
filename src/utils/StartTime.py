"""
    Contains the data for an activity's start time
    ** UNUSED **
"""


class StartTime:
    def __init__(self, str):
        """Create a Time object given a StarDate field from the API"""
        index = str.index('T')
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
