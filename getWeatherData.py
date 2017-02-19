import myNOAA
import json
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime

# create client
noaa = myNOAA.noaa()
states = noaa.getStateIDs()


noaa.getAllData(startTime=datetime(1900, 1, 1))
noaa.save(fileName="georgiaTemps.p")
print noaa.data




