import os

import pymssql
from dotenv import load_dotenv


def convertTime(datetime):
    """Converts a datetime object to a more readable time."""
    index = datetime.index(' ') + 1
    datetime = datetime[index:]
    hour = datetime[0:2]
    period = ''
    if int(hour) >= 12:
        period = 'PM'
        if int(hour) != 12:
            hour = str(int(hour) - 12)
    else:
        period = 'AM'
    return hour + ':' + datetime[3:5] + ' ' + period


class Schedule:
    def __init__(self, env_dir):
        self.scheduledActivities = {}
        load_dotenv(dotenv_path=env_dir)
        db_server = os.getenv("DB_SERVER")
        db_username = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASS")
        conn = pymssql.connect(server=db_server, port='1433', user=db_username, password=db_password,
                               database='Tableau')
        cursor = conn.cursor()
        cursor.execute("""SELECT e.EstablishmentName, t.StartDateTime FROM dbo.Establishments e
                        JOIN dbo.TimeTable t ON e.EstablishmentId = t.EstablishmentId
                        WHERE StartDateTime > CURRENT_TIMESTAMP AND CAST(t.StartDateTime AS TIME) <= '20:00:00.000'""")
        for obj in cursor.fetchall():
            estName = obj[0]
            schedTime = convertTime(str(obj[1]))
            self.scheduledActivities[estName] = schedTime

    def getScheduledAct(self, establishment):
        return self.scheduledActivities.get(establishment)
