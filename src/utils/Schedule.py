import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions


class Schedule:
    def __init__(self):
        self.scheduledActivities = {}
        options = EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('headless')
        driver = webdriver.Edge(options=options)
        driver.get('https://schedule.kidzaniausa.com/')
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        tags = soup.find_all('h3')
        times = soup.find_all('time')
        i = 0
        for tag in tags:
            self.scheduledActivities[tag.string] = times[i].string
            i += 1


    def getScheduledAct(self, establishment):
        return self.scheduledActivities.get(establishment)
