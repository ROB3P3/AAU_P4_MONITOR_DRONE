import matplotlib.pyplot as plt
import pandas
import numpy as np
import math
import os
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from scipy.interpolate import interp1d

testNumber = 11
refX = 0
refY = 0
refZ = 155

pathToViconCSV = "./Real/Data Processing/Hover tests/Hover Test " + str(testNumber) + ".csv"

csvFileVicon = pandas.read_csv(pathToViconCSV, skiprows=[0, 1, 2, 4], usecols=['Frame', 'TX', 'TY', 'TZ'], skip_blank_lines=True)

os.makedirs("./Real/Data Processing/Hover tests/Test figures/Test " + str(testNumber), exist_ok=True)
os.chdir("./Real/Data Processing/Hover tests/Test figures/Test " + str(testNumber))

print("Visualizing data for test " + str(testNumber))

# remove any frames where vicon did not pick up data
for i in range(len(csvFileVicon['Frame'])):
    if math.isnan(csvFileVicon['TX'][i]):
        csvFileVicon = csvFileVicon.drop(i)

csvFileVicon = csvFileVicon.reset_index()

# determine the start and end points of the drone path (vicon)
# this is determined to be +- 5 in x and y and 95 to 115 in z
pathStartPoint = 2000
pathEndPoint = 3000 #len(csvFileVicon['Frame'].to_numpy()) - 1

""" for i in range(len(csvFileVicon['Frame'])):
    xCoord = csvFileVicon['TX'][i] / 10
    yCoord = csvFileVicon['TY'][i] / 10
    zCoord = csvFileVicon['TZ'][i] / 10
    if pathStartPoint == 0 and zCoord > refZ - 3 and zCoord + 3:
        print("Drone path start (pos ~= [0, 0, 100]):", i, xCoord, yCoord, zCoord)
        pathStartPoint = i
    if pathStartPoint != 0 and pathEndPoint == 0 and i > pathStartPoint + 2000 and zCoord < refZ - 3:
        print("Drone path end (pos ~= [0, 0, 100]):", i, xCoord, yCoord, zCoord)
        pathEndPoint = i + 1
        break """

# limit to start and end point prev determined to remove ascent and descent from the drone path (vicon)
csvFileViconXYPath = csvFileVicon.iloc[pathStartPoint:pathEndPoint]
csvFileViconXYPath = csvFileViconXYPath.reset_index()

viconXY = np.vstack(csvFileViconXYPath[['TX', 'TY', 'TZ']].to_numpy(), dtype=np.float64)


xErrors = []
yErrors = []
zErrors = []
totalErrors = []
highestXError = 0
highestYError = 0
highestZError = 0
highestTotError = 0

for i in range(len(csvFileViconXYPath['TX'])):
    xErr = abs((csvFileViconXYPath['TX'][i] / 10) - refX)
    yErr = abs((csvFileViconXYPath['TY'][i] / 10) - refY)
    zErr = abs((csvFileViconXYPath['TZ'][i] / 10) - refZ)
    xErrors.append(xErr)
    yErrors.append(yErr)
    zErrors.append(zErr)

    totErr = np.sqrt(xErr**2 + yErr**2 + zErr**2)
    totalErrors.append(totErr)

    if xErr > highestXError:
        highestXError = xErr
    if  yErr > highestYError:
        highestYError = yErr
    if zErr > highestZError:
        highestZError = zErr
    if totErr > highestTotError:
        highestTotError = totErr

#totalErrors = np.sqrt(np.array(xErrors)**2 + np.array(yErrors)**2 + np.array(zErrors)**2)

meanXError = np.mean(xErrors)
print(f"Mean x error: {meanXError}")
print(f"Highest x error: {highestXError}")
meanYError = np.mean(yErrors)
print(f"Mean y error: {meanYError}")
print(f"Highest y error: {highestYError}")
meanZError = np.mean(zErrors)
print(f"Mean z error: {meanZError}")
print(f"Highest z error: {highestZError}")
meanTotalError = np.mean(totalErrors)
print(f"Mean total error: {meanTotalError}")
print(f"Highest total error: {highestTotError}")

# X over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel('x (cm)')
plt.title('Plot of X over time')
plt.grid(True)

plt.plot(csvFileViconXYPath['Frame'].to_numpy(), csvFileViconXYPath['TX'].to_numpy()/10, color='Blue')
plt.plot(csvFileViconXYPath['Frame'].to_numpy(), [refX for i in range(len(csvFileViconXYPath['Frame']))], color='Red')
#plt.plot([csvFileViconXYPath['Frame'].to_numpy()[pathStartPoint]], [csvFileViconXYPath['TX'].to_numpy()[pathStartPoint]/10], marker='*', ls='none', ms=10, color='Purple')
#plt.plot([csvFileViconXYPath['Frame'].to_numpy()[pathEndPoint]], [csvFileViconXYPath['TX'].to_numpy()[pathEndPoint]/10], marker='*', ls='none', ms=10, color='Orange')

fig.savefig("X over time.png")

# Y over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel('y (cm)')
plt.title('Plot of Y over time')
plt.grid(True)

plt.plot(csvFileViconXYPath['Frame'].to_numpy(), csvFileViconXYPath['TY'].to_numpy()/10, color='Blue')
plt.plot(csvFileViconXYPath['Frame'].to_numpy(), [refX for i in range(len(csvFileViconXYPath['Frame']))], color='Red')
#plt.plot([csvFileViconXYPath['Frame'].to_numpy()[pathStartPoint]], [csvFileViconXYPath['TY'].to_numpy()[pathStartPoint]/10], marker='*', ls='none', ms=10, color='Purple')
#plt.plot([csvFileViconXYPath['Frame'].to_numpy()[pathEndPoint]], [csvFileViconXYPath['TY'].to_numpy()[pathEndPoint]/10], marker='*', ls='none', ms=10, color='Orange')

fig.savefig("Y over time.png")

# Z over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel('z (cm)')
plt.title('Plot of Z over time')
plt.grid(True)

plt.plot(csvFileViconXYPath['Frame'].to_numpy(), csvFileViconXYPath['TZ'].to_numpy()/10, color='Blue')
plt.plot(csvFileViconXYPath['Frame'].to_numpy(), [refZ for i in range(len(csvFileViconXYPath['Frame']))], color='Red')
#plt.plot([csvFileViconXYPath['Frame'].to_numpy()[pathStartPoint]], [csvFileViconXYPath['TZ'].to_numpy()[pathStartPoint]/10], marker='*', ls='none', ms=10, color='Purple')
#plt.plot([csvFileViconXYPath['Frame'].to_numpy()[pathEndPoint]], [csvFileViconXYPath['TZ'].to_numpy()[pathEndPoint]/10], marker='*', ls='none', ms=10, color='Orange')

fig.savefig("Z over time.png")

# Y over X plot
fig, ax = plt.subplots()
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.title('Plot of Y over X')
plt.grid(True)

plt.plot(viconXY[:, 0] / 10, viconXY[:, 1] / 10, color='Blue')
#plt.plot([csvFileViconXYPath['TX'].to_numpy()[0]/10], [csvFileViconXYPath['TY'].to_numpy()[0]/10], marker='*', ls='none', ms=10, color='Purple')
#plt.plot([csvFileViconXYPath['TX'].to_numpy()[-1]/10], [csvFileViconXYPath['TY'].to_numpy()[-1]/10], marker='*', ls='none', ms=10, color='Orange')

fig.savefig("Y over X.png")

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x (cm)')
ax.set_ylabel('y (cm)')
ax.set_zlabel('z (cm)')
ax.set_title('3D plot of path')

ax.plot(csvFileVicon['TX'].to_numpy()/10, csvFileVicon['TY'].to_numpy()/10, csvFileVicon['TZ'].to_numpy()/10, color='Black')
ax.plot([csvFileVicon['TX'].to_numpy()[0]/10], [csvFileVicon['TY'].to_numpy()[0]/10], [csvFileVicon['TZ'].to_numpy()[0]/10], marker='*', ls='none', ms=10, color='Green')
ax.plot([csvFileVicon['TX'].to_numpy()[-1]/10], [csvFileVicon['TY'].to_numpy()[-1]/10], [csvFileVicon['TZ'].to_numpy()[-1]/10], marker='*', ls='none', ms=10, color='Blue')
ax.plot([csvFileVicon['TX'].to_numpy()[0]/10], [csvFileVicon['TY'].to_numpy()[0]/10], [csvFileVicon['TZ'].to_numpy()[0]/10], marker='*', ls='none', ms=10, color='Purple')
ax.plot([csvFileVicon['TX'].to_numpy()[-1]/10], [csvFileVicon['TY'].to_numpy()[-1]/10], [csvFileVicon['TZ'].to_numpy()[-1]/10], marker='*', ls='none', ms=10, color='Orange')

fig.savefig("3D plot.png")

plt.show()