import myNOAA
import json
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime

# create client
noaa=myNOAA.noaa()

dailySums = noaa.getData(30528)


with open('dailySums.txt', 'w') as outfile:
    json.dump(dailySums, outfile)

