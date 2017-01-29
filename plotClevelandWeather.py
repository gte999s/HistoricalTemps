import myNOAA
import json
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime

# create client
noaa = myNOAA.noaa()

print "sending request"
dailySums = noaa.getData(30528)

file = open('dailySums.html', 'w')
file.write(dailySums.text)
file.close()

with open('dailySums.json', 'w') as outfile:
    json.dump(dailySums.json(), outfile)


