"""
    Manages the data for a date
"""


class Date:
    def __init__(self, str):
        """Create a Date object given a StarDate from the API"""
        self.month = str[5:7]
        self.day = str[8:10]
        self.year = str[:4]

    def __str__(self):
        """Returns the string as mm/dd/yyyy. Leading 0's in the month/day are removed."""
        return f"{int(self.month)}/{int(self.day)}/{self.year}"


    def monthAsInt(self):
        """Return the month as an integer"""
        return int(self.month)

    def dayAsInt(self):
        """Return the day as an integer"""
        return int(self.day)

    def yearAsInt(self):
        """Return the year as an integer"""
        return int(self.year)
