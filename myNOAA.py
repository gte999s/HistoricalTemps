
import requests
import pandas
import cPickle as pickle
from datetime import datetime
from datetime import timedelta

# this is Hanna's code. Hahahahaha. Mine!

def load(pickleFileName = "weatherData.p"):
    file = open(pickleFileName, 'rb')
    noaaObj = pickle.load(file)
    file.close()
    return noaaObj


class noaa:
    def __init__(self):
        self.token = "VaxmiYwCHiVWYivnDhkrMIWUSmUMsVSa"
        self.dataSet = "GHCND"
        self.units = 'standard'
        self.requestURL = "http://www.ncdc.noaa.gov/cdo-web/api/v2/"
        self.data = pandas.DataFrame()
        self.requestedDataNum = None
        self.receivedDataNum = 0
        self.locationID = 'FIPS:13'

    def save(self, fileName = "weatherData.p"):
        print "Saving to File: " + fileName
        file = open(fileName, 'wb')
        pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)
        file.close()

    def getAllData(self, startTime=datetime(1900,1,1), endTime=datetime.now()):
        self.startTime = startTime
        self.endTime = endTime
        startTimeTemp = startTime
        endTimeTemp = startTime

        while endTimeTemp < endTime:
            startTimeTemp = endTimeTemp
            endTimeTemp = endTimeTemp + timedelta(days=365)

            if endTimeTemp > endTime:
                endTimeTemp = endTime

            print "Getting Data for {start} to {end}".format(start=startTimeTemp.strftime('%Y-%m-%d'),
                                                             end=endTimeTemp.strftime('%Y-%m-%d'))

            self.getData(startTime=startTimeTemp, endTime=endTimeTemp)

    def getStateIDs(self):
        headers = {'token': self.token}
        url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=ST&datasetid=GHCND&limit=1000'
        needData = True
        totalData = 0

        while needData:
            print "Sending Request"
            response = requests.get(url, headers=headers)
            if response.status_code == 502:
                print "Service is Unavailable, retrying"

            else:
                needData = False
                print "Data Received"
                return response.json()

    def getData(self, startTime=datetime(2000,1,1), endTime=datetime(2000,2,1)):
        customPart = "data?datasetid={dataSet}&locationid={locationID}&startdate={startDate}&enddate={endDate}" \
                     "&limit=1000&datatypeid=TMAX&datatypeid=TMIN&units={units}&offset={offset}"

        url = self.requestURL + customPart.format(dataSet=self.dataSet,
                                                  locationID=self.locationID,
                                                  startDate=startTime.strftime('%Y-%m-%dT%H:%M:%S'),
                                                  endDate=endTime.strftime('%Y-%m-%dT%H:%M:%S'),
                                                  units=self.units,
                                                  offset=self.receivedDataNum)
        headers = {'token': self.token}
        needData = True
        totalData = 0
        print url

        while needData:
            print "Sending Request"
            response = requests.get(url, headers=headers)
            if response.status_code == 502:
                print "Service is Unavailable, retrying"

            else:
                needData = False
                print "Data Received"
                data = response.json()
                if data.__len__() == 0:
                    print "No Data for Date Range"
                    continue

                self.data = self.data.append(data['results'])
                if self.requestedDataNum is None:
                    self.requestedDataNum = data['metadata']['resultset']['count']

                self.receivedDataNum += data['results'].__len__()  + 1

        if self.receivedDataNum < self.requestedDataNum:
            print "Asking for more data to complete request {percent}% Complete".format(percent=100*self.receivedDataNum/self.requestedDataNum)
            self.getData( startTime=startTime, endTime=endTime)

        else:
            self.receivedDataNum = 0
            self.requestedDataNum = None



