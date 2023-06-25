"""
    This class is responsible for making the API requests storing the response.
    As the "lovely" FourZ API loves to confuse you, "population" refers to establishment guests, and "attendance"
        refers to total park guests.
"""

import requests
import Activity
from dotenv import load_dotenv
import os
import json


class ActivityRequest:
    def __init__(self, park) -> None:
        self.park = park
        abs_path = os.path.abspath(__file__)  # Absolute path to the file
        current_dir = abs_path
        while current_dir[len(current_dir) - 13:] != "BekhaTelegram":  # Find the BEKHA directory
            current_dir = os.path.dirname(current_dir)
            if current_dir == "C:\\":  # Stop an endless loop if the folder isn't found
                print('Directory "BekhaTelegram" not found in project.')
                break
        self.env_file_path = os.path.join(current_dir, ".env")
        self.activity_info_file_path = os.path.join(current_dir, "files", "ActivityInfo.json")
        self.image_file_path = os.path.join(current_dir, "files", "bek.png")
        load_dotenv(dotenv_path=self.env_file_path)
        self.username = os.getenv("USER_NAME")
        self.password = os.getenv("PASSWORD")
        # Initialize variables
        self.token = 0
        self.totalInActivities = 0
        self.activeEstablishments = 0
        self.attendees = 0
        self.minorAttendees = 0
        # Call set up methods
        self.getAuth()  # Get API key
        self.config()  # Set up request information after API key is received
        content = self.makeRequest('population')  # Request from population API and save it temporarily
        self.parsePopulation(content)  # Parse the response and save it in activities list
        self.parseAttendance(self.makeRequest('attendance'))  # Parse the response
        self.sortActDec()  # Sort the activities list


    def config(self):
        self.payloadPopulation = f'''<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
            <Header>
                <authentication-header xmlns="kidzania.com" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
                    <Token xmlns="http://schemas.datacontract.org/2004/07/KZoftware.Services.Behaviors">{self.token}</Token>
                </authentication-header>
            </Header>
            <Body>
                <CurrentActivityAfluence xmlns="http://tempuri.org/">
                    <facilityID>acd1e2e5-a306-41fe-88f8-1ef78dba23a7</facilityID>
                </CurrentActivityAfluence>
            </Body>
            </Envelope>'''
        self.headerPopulation = {
            'SOAPAction': "http://tempuri.org/IEstablishmentOperationService/CurrentActivityAfluence",
            'content-type': 'text/xml; charset="utf-8"'}
        self.urlPopulation = 'https://www.fourz.net:8443/Operations/EstablishmentOperationService.svc'
        self.payloadAttendance = f'''<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
            <Header>
                <authentication-header xmlns="kidzania.com" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
                    <Token xmlns="http://schemas.datacontract.org/2004/07/KZoftware.Services.Behaviors">704d3a13-0939-4f26-bf31-bac3c8c54afc</Token>
                </authentication-header>
            </Header>
            <Body>
                <GetAttendance xmlns="http://tempuri.org/">
                    <FacilityID>acd1e2e5-a306-41fe-88f8-1ef78dba23a7</FacilityID>
                </GetAttendance>
            </Body>
            </Envelope>'''
        self.headerAttendance = {'SOAPAction': "http://tempuri.org/IAttendanceService/GetAttendance",
                                 'content-type': 'text/xml; charset="utf-8"'}
        self.urlAttendance = 'https://www.fourz.net:8443/POS/AttendanceManagementService.svc'


    def getAuth(self):
        """Obtain an API key (token) for other requests"""
        self.payloadValidate = f'''<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
            <Body>
                <ValidateUserCredentials xmlns="http://tempuri.org/">
                    <userName>{self.username}</userName>
                    <password>{self.password}</password>
                </ValidateUserCredentials>
            </Body>
            </Envelope>'''
        self.headerValidate = {'SOAPAction': "http://tempuri.org/IIdentityManagementService/ValidateUserCredentials",
                               'content-type': 'text/xml; charset=utf-8'}
        try:  # VITA tries to make a post request to the URL
            # Make the request and store the raw data
            request = requests.request("POST", url='https://www.fourz.net:8443/Identity/IdentityManagementService.svc',
                                       data=self.payloadValidate, headers=self.headerValidate)
            content = str(request.content)  # Parse response into a string
            # Token is retrieved from the main content
            self.token = content[content.index('KZoftware.Services.Behaviors">') + 30: content.index(
                'KZoftware.Services.Behaviors">') + 66]
        except requests.exceptions.ConnectTimeout:  # Timeout error (BEKHA took too long)
            self.results(('Connection Timed Out', False))
        except requests.exceptions.ConnectionError:  # Connection error
            self.results(('Connection Failed, try reconnecting to the network', False))


    def makeRequest(self, type):
        """Make a request given the type. Types: 'population', 'attendance'"""
        type = type.lower()
        if type == 'population':
            payload = self.payloadPopulation
            header = self.headerPopulation
            url = self.urlPopulation
        elif type == 'attendance':
            payload = self.payloadAttendance
            header = self.headerAttendance
            url = self.urlAttendance
        else:
            print(f"Error in makeRequest({type}), type is invalid")
            return
        request = requests.request("POST", url=url, data=payload, headers=header)  # Make the request and store raw data
        content = str(request.content)  # Parse the response into a string
        try:  # Attempt to return the content
            return content
        except ValueError:  # If the information is not found, attempt again with a new key
            self.getAuth()  # Grab a new key
            self.config()  # Reconfigure the request information
            request = requests.request("POST", url=url, data=payload, headers=header)  # Request and store data again
            content = str(request.content)  # Parse the response into string
            return content  # Return the content again
        except requests.exceptions.ConnectTimeout:
            return 'Connection Timed Out'
        except requests.exceptions.ConnectionError:
            return 'Connection Failed, try reconnecting to the network'


    def parsePopulation(self, response):
        """Parse the response from population and populate the activities array"""
        while response.find('<b:ActivityAffluenceDTO>') != -1:  # Create the Activity objects a
            response = response[response.index('<b:ActivityAffluenceDTO>'):]
            actID = response[response.index('<b:ActivityID>') + 14:response.index('</b:ActivityID>')]
            currActGuests = response[
                            response.index('<b:CurrentAffluence>') + 20:response.index('</b:CurrentAffluence>')]
            self.createActivity(response, actID, currActGuests)
            self.park.guestsInActivities += int(currActGuests)  # Increase total guests in activities
            if int(currActGuests) > 0:  # Check if the establishment has guests, increase activeEstablishments if so
                self.park.activeEstablishments += 1
            response = response[response.index('</b:ActivityAffluenceDTO>'):]


    def parseAttendance(self, response):
        """Parse the response from attendance"""
        self.park.currentGuests = response[response.index('<b:Attendees>') + 13:response.index('</b:Attendees>')]
        self.park.currentKids = response[response.index('<b:MinorAttendees>') + 18:response.index('</b:MinorAttendees>')]


    def createActivity(self, response, id, currGuests):
        """Create a new Activity and add it to the activities given its ID and current number of guests"""
        act = self.findActivityByID(id)
        if act == 'NotFound':
            actName = response[response.index('<b:ActivityName>') + 16:response.index('</b:ActivityName>')]
            estName = response[response.index('<b:EstablishName>') + 17:response.index('</b:EstablishName>')]
            maxGuests = 0
            open = True
            print(f'Activity {actName} at {estName} is not in the json file.')
        else:
            actName = act['ActivityName']
            estName = act['EstablishName']
            maxGuests = act['MaxGuests']
            open = act['IsOpen']
        newAct = Activity.Activity(actName, estName, int(currGuests), open, maxGuests)
        self.park.addActivity(newAct)


    def findActivityByID(self, id):
        """Given an ActivityID, finds and returns the json data"""
        with open(self.activity_info_file_path, 'r') as file:
            json_data = file.read()
        data = json.loads(json_data)
        for item in data['ActivityAffluenceDTO']:
            if item['ActivityID'] == id:
                return item
        return 'NotFound'


    def sortActInc(self):
        """Sorts the activities by activity in increasing order"""
        if (n := len(self.park.activities)) <= 1:
            return
        for i in range(1, n):
            key = self.park.activities[i]
            j = i - 1
            while j >= 0 and int(key.currentGuests) < int(self.park.activities[j].currentGuests):
                self.park.activities[j + 1] = self.park.activities[j]
                j -= 1
            self.park.activities[j + 1] = key

    def sortActDec(self):
        """Sorts the activities by activity in decreasing order"""
        if (n := len(self.park.activities)) <= 1:
            return
        for i in range(1, n):
            key = self.park.activities[i]
            j = i - 1
            while j >= 0 and int(key.currentGuests) > int(self.park.activities[j].currentGuests):
                self.park.activities[j + 1] = self.park.activities[j]
                j -= 1
            self.park.activities[j + 1] = key


    def sortEst(self):
        """Sorts the activities by establishment"""
        if (n := len(self.park.activities)) <= 1:
            return
        for i in range(1, n):
            key = self.park.activities[i]
            j = i - 1
            while j >= 0 and key.establishmentName < self.park.activities[j].establishmentName:
                self.park.activities[j + 1] = self.park.activities[j]
                j -= 1
            self.park.activities[j + 1] = key
