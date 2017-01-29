
import requests


class noaa:

    def __init__(self, startYear="2016", startMonth="12", startDay="01", endYear="2017",endMonth="01",endDay="01"):
        self.token = "VaxmiYwCHiVWYivnDhkrMIWUSmUMsVSa"
        self.startTime = startYear + "-" + startMonth + "-" + startDay
        self.endTime   = endYear + "-" + endMonth + "-" + endDay
        self.dataSet = "GHCND"
        self.requestURL = "http://www.ncdc.noaa.gov/cdo-web/api/v2/"

    def getData(self, zipCode):
        customPart = "data?datasetid={dataSet}&locationid=ZIP:{zip}&startdate={startDate}&enddate={endDate}&limit=1000"
        url = self.requestURL + customPart.format(dataSet=self.dataSet,
                                                  zip=zipCode,
                                                  startDate=self.startTime,
                                                  endDate=self.endTime)
        headers = {'token': self.token}
        response = requests.get(url, headers=headers)
        print url
        return response
