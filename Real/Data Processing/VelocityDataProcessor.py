import matplotlib.pyplot as plt
import pandas
import numpy as np
import math
import os
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from scipy.interpolate import interp1d

testNumber = 13

pathToViconCSV = "./Real/Data Processing/Gode tests/Vicon Test " + str(testNumber) + ".csv"

csvFileVicon = pandas.read_csv(pathToViconCSV, skiprows=[0, 1, 2, 4], usecols=['Frame', 'TX', 'TY', 'TZ'], skip_blank_lines=True)

os.makedirs("./Real/Data Processing/Velocity tests/Test figures/Test " + str(testNumber), exist_ok=True)
os.chdir("./Real/Data Processing/Velocity tests/Test figures/Test " + str(testNumber))

print("Visualizing data for test " + str(testNumber))

velRef = 10 # cm/s 
deltaT = 0.01 # seconds

# vicon 1 frame = 5 ms (test 1-7)
# vicon 100 frames = 0.5 second (test 1-7)
# vicon 1 frame = 10 ms (test 8-13)
# vicon 100 frames = 1 second (test 8-13)

# remove any frames where vicon did not pick up data
for i in range(len(csvFileVicon['Frame'])):
    if math.isnan(csvFileVicon['TX'][i]):
        csvFileVicon = csvFileVicon.drop(i)

csvFileVicon = csvFileVicon.reset_index()

# determine the start and end points of the drone path (vicon)
# this is determined to be +- 5 in x and y and 95 to 115 in z
pathStartPoint = 0
pathEndPoint = 0
for i in range(len(csvFileVicon['Frame'])):
    xCoord = csvFileVicon['TX'][i] / 10
    yCoord = csvFileVicon['TY'][i] / 10
    zCoord = csvFileVicon['TZ'][i] / 10
    if pathStartPoint == 0 and xCoord > -10 and xCoord < 10 and yCoord > -10 and yCoord < 10 and zCoord > 95 and zCoord < 115:
        print("Drone path start (pos ~= [0, 0, 100]):", i, xCoord, yCoord, zCoord)
        pathStartPoint = i
    if pathStartPoint != 0 and pathEndPoint == 0 and i > pathStartPoint + 5000 and xCoord > -10 and xCoord < 10 and yCoord > -10 and yCoord < 10 and zCoord < 105:
        print("Drone path end (pos ~= [0, 0, 100]):", i, xCoord, yCoord, zCoord)
        pathEndPoint = i + 1
        break

# limit to start and end point prev determined to remove ascent and descent from the drone path (vicon)
csvFileViconXYPath = csvFileVicon.iloc[pathStartPoint:pathEndPoint]
csvFileViconXYPath = csvFileViconXYPath.reset_index()

# convert to [X, Y] arrays
viconXY = np.vstack(csvFileViconXYPath[['TX', 'TY']].to_numpy(), dtype=np.float64)

velocityX = []
velocityY = []
velocityXY = []

velErrorX = []
velErrorY = []
velErrorXY = []

highestVelErrorX = 0
highestVelErrorY = 0
highestVelErrorXY = 0

for i in range(len(viconXY) - 1):
    xCoord = viconXY[i][0] / 10
    yCoord = viconXY[i][1] / 10

    xCoordNext = viconXY[i + 1][0] / 10
    yCoordNext = viconXY[i + 1][1] / 10

    velX = abs(xCoordNext - xCoord) / deltaT
    velY = abs(yCoordNext - yCoord) / deltaT
    velXY = np.sqrt(velX ** 2 + velY ** 2)

    velocityX.append(velX)
    velocityY.append(velY)
    velocityXY.append(velXY)

    velErrorX.append(abs(velX - velRef))
    velErrorY.append(abs(velY - velRef))
    velErrorXY.append(abs(velXY - velRef))

    if abs(velX - velRef) > highestVelErrorX:
        highestVelErrorX = abs(velX - velRef)
    if abs(velY - velRef) > highestVelErrorY:
        highestVelErrorY = abs(velY - velRef)
    if abs(velXY - velRef) > highestVelErrorXY:
        highestVelErrorXY = abs(velXY - velRef)
        

velocityX = np.array(velocityX)
velocityY = np.array(velocityY)
velocityXY = np.array(velocityXY)

velErrorX = np.array(velErrorX)
velErrorY = np.array(velErrorY)
velErrorXY = np.array(velErrorXY)

meanVelX = np.mean(velocityX)
meanVelY = np.mean(velocityY)
meanVelXY = np.mean(velocityXY)

meanVelErrorX = np.mean(velErrorX)
meanVelErrorY = np.mean(velErrorY)
meanVelErrorXY = np.mean(velErrorXY)

print("Mean x velocity:", meanVelX)
print("Mean x velocity error:", meanVelErrorX)
print("Highest x velocity error:", highestVelErrorX)

print("Mean y velocity:", meanVelY)
print("Mean y velocity error:", meanVelErrorY)
print("Highest y velocity error:", highestVelErrorY)

print("Mean velocity:", meanVelXY)
print("Mean velocity error:", meanVelErrorXY)
print("Highest velocity error:", highestVelErrorXY)

csvFileViconXYPath = csvFileViconXYPath.head(-1)

# X vel over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel("x' (cm/s)")
plt.title('Plot of x velocity over time')
plt.grid(True)

plt.plot(csvFileViconXYPath['Frame'].to_numpy(), velocityX, color='Blue')
plt.plot(csvFileViconXYPath['Frame'].to_numpy(), [velRef for i in range(len(csvFileViconXYPath['Frame']))], color='Red')

fig.savefig("X vel over time.png")

# Y vel over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel("y' (cm/s)")
plt.title('Plot of y velocity over time')
plt.grid(True)

plt.plot(csvFileViconXYPath['Frame'].to_numpy(), velocityY, color='Blue')
plt.plot(csvFileViconXYPath['Frame'].to_numpy(), [velRef for i in range(len(csvFileViconXYPath['Frame']))], color='Red')

fig.savefig("Y vel over time.png")

# XY vel over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel("v (cm/s)")
plt.title('Plot of velocity over time')
plt.grid(True)
plt.plot(csvFileViconXYPath['Frame'].to_numpy(), velocityXY, color='Blue')
plt.plot(csvFileViconXYPath['Frame'].to_numpy(), [velRef for i in range(len(csvFileViconXYPath['Frame']))], color='Red')

fig.savefig("Velocity over time.png")

plt.show()