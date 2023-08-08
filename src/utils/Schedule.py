import os

import pymssql
from dotenv import load_dotenv


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
        cursor.execute("select * from TimeTable where TimeTable.StartDateTime > CURRENT_TIMESTAMP;")
        #for obj in cursor.fetchall():
        #    self.scheduledActivities[]
        print(cursor.fetchall())


    def getScheduledAct(self, establishment):
        return self.scheduledActivities.get(establishment)


Schedule("C:\\Users\\riley.bagwell\\PycharmProjects\\BekhaTelegram\\.env")
