import myNOAA
import json
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime

# create client
noaa = myNOAA.noaa()

noaa.getAllData(startTime=datetime(1900,1,1))
noaa.save()



