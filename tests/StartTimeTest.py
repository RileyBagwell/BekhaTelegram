"""
    Test StartTime class by creating an instance of this class.
    Note that the syntax from FourZ for StarDate is yyyy-mm-ddThh:mm:ss.ss,
        where T separates the date from the time. s is seconds with an unknown number of digits after decimal
"""

from src.utils.StartTime import StartTime


class StartTimeTest:
    def __init__(self):
        time1Str = "2023-06-28T18:09:11.38"
        time2Str = "2002-10-07T08:12:43"
        time1 = StartTime(time1Str)
        time2 = StartTime(time2Str)
        print(time1Str + " reformatted: " + time1.__str__())
        print(time2Str + " reformatted: " + time2.__str__())
