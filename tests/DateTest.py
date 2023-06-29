"""
    Test DateTest class by creating an instance of this class.
    Note that the syntax from FourZ for StarDate is yyyy-mm-ddThh:mm:ss.ss,
        where T separates the date from the time. s is seconds with an unknown number of digits after decimal
"""

from src.utils.Date import Date


class DateTest:
    def __init__(self):
        date1Str = "2023-06-28T18:09:11.38"
        date2Str = "2002-10-07T06:12:43"
        date1 = Date(date1Str)
        date2 = Date(date2Str)
        print(date1Str + " reformatted: " + date1.__str__())
        print(date2Str + " reformatted: " + date2.__str__())
