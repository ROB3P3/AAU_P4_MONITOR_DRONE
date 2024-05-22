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
pathToPathPlannerCSV = "./Real/Data Processing/Gode tests/PathData test " + str(testNumber) + ".csv"

csvFileVicon = pandas.read_csv(pathToViconCSV, skiprows=[0, 1, 2, 4], usecols=['Frame', 'TX', 'TY', 'TZ'], skip_blank_lines=True)
csvFilePathPlanner = pandas.read_csv(pathToPathPlannerCSV)

os.makedirs("./Real/Data Processing/Gode tests/Test figures/Test " + str(testNumber), exist_ok=True)
os.chdir("./Real/Data Processing/Gode tests/Test figures/Test " + str(testNumber))

print("Visualizing data for test " + str(testNumber))

# vicon 1 frame = 5 ms (test 1-7)
# vicon 100 frames = 0.5 second (test 1-7)
# vicon 1 frame = 10 ms (test 8-13)
# vicon 100 frames = 1 second (test 8-13)

# source to interpolation: https://en.wikipedia.org/wiki/Interpolation
# another: https://www.youtube.com/watch?v=RpxoN9-i7Jc
# interpolation is used to scale up the path planner's path to 1000 points and 
# scale down the drone path (vicon) down to 5000 points to be able to compare to the path planner's path
def interpolatePath(path, num_points):
    distances = np.sqrt(np.sum(np.diff(path, axis=0)**2, axis=1))
    cumulDistances = np.insert(np.cumsum(distances), 0, 0)
    interpolFunc = interp1d(cumulDistances, path, axis=0, kind='linear')
    interpolDistances = np.linspace(0, cumulDistances[-1], num_points)
    interpolPath = interpolFunc(interpolDistances)
    return interpolPath

# source to dynamic time warping: https://builtin.com/data-science/dynamic-time-warping
# dynamic time warping is used to compare the path planner's path and the drone path (vicon)
def calculate_dtw_errors(goalPath, actualPath):
    # Use DTW to find the best alignment between the goal and actual paths
    distance, path = fastdtw(goalPath, actualPath, dist=euclidean)
    
    # Extract aligned coordinates
    goalAlignedPoints = np.array([goalPath[i] for i, _ in path])
    actualAlignedPoints = np.array([actualPath[j] for _, j in path])
    
    # Calculate x and y errors
    x_errors = abs(actualAlignedPoints[:, 0] - goalAlignedPoints[:, 0])
    y_errors = abs(actualAlignedPoints[:, 1] - goalAlignedPoints[:, 1])
    
    return x_errors, y_errors

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
    if pathStartPoint != 0 and pathEndPoint == 0 and i > pathStartPoint + 10000 and xCoord > -10 and xCoord < 10 and yCoord > -10 and yCoord < 10 and zCoord < 105:
        print("Drone path end (pos ~= [0, 0, 100]):", i, xCoord, yCoord, zCoord)
        pathEndPoint = i + 1
        break

# limit to start and end point prev determined to remove ascent and descent from the drone path (vicon)
csvFileViconXYPath = csvFileVicon.iloc[pathStartPoint:pathEndPoint]
csvFileViconXYPath = csvFileViconXYPath.reset_index()

# determine end point for path planner path (0, 0, 100)
pathPlannerEnd = 0
for i in range(len(csvFilePathPlanner['Time'])):
    if i > 20 and csvFilePathPlanner['TX'][i] == 0 and csvFilePathPlanner['TY'][i] == 0 and csvFilePathPlanner['TZ'][i] == 100:
        pathPlannerEnd = i + 1
        break

# limit path planner path so it starts at (0, 0, 100) and ends at (0, 0, 100) so ascent and descent is not considered
csvFilePathPlanner = csvFilePathPlanner.iloc[20:pathPlannerEnd]
csvFilePathPlanner = csvFilePathPlanner.reset_index()

# convert to [X, Y] arrays
pathPlannerXY = np.vstack(csvFilePathPlanner[['TX', 'TY']].to_numpy(), dtype=np.float64)
viconXY = np.vstack(csvFileViconXYPath[['TX', 'TY']].to_numpy(), dtype=np.float64)
# interpolate path planner's path to 1000 points and vicon drone path to 5000 points to be able to perform dynamic time warping
interpolatedPathPlannerXY = interpolatePath(pathPlannerXY, 1000)
interpolatedViconXY = interpolatePath(viconXY, 5000)

# calculate errors in x and y direction
xErrors, yErrors = calculate_dtw_errors(interpolatedPathPlannerXY, interpolatedViconXY / 10)
# calculate total error as the square root of the sum of the squares of the x and y errors
totalErrors = np.sqrt(xErrors ** 2 + yErrors ** 2)

# find the points with an error greater than 5
highErrorPoints = []
highestError = 0
for i, err in enumerate(totalErrors):
    if err > 5:
        try:
            highErrorPoints.append(interpolatedViconXY[i])
        except IndexError:
            continue
    if err > highestError:
        highestError = err

highErrorPoints = np.array(highErrorPoints)

# calculate the mean error
meanError = np.mean(totalErrors)
print(f"Mean error: {meanError}")
print(f"Highest error: {highestError}")

refZ = 105
zErrors = []
highestZError = 0

for i in csvFileViconXYPath['TZ']:
    i = i / 10
    zErrors.append(abs(i - refZ))
    if abs(i - refZ) > highestZError:
        highestZError = abs(i - refZ)

meanZError = np.mean(zErrors)
print(f"Mean z error: {meanZError}")
print(f"Highest z error: {highestZError}")

# X over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel('x (cm)')
plt.title('Plot of X over time')
plt.grid(True)

plt.plot(csvFileVicon['Frame'].to_numpy(), csvFileVicon['TX'].to_numpy()/10, color='Black')
plt.plot([csvFileVicon['Frame'].to_numpy()[pathStartPoint]], [csvFileVicon['TX'].to_numpy()[pathStartPoint]/10], marker='*', ls='none', ms=10, color='Purple')
plt.plot([csvFileVicon['Frame'].to_numpy()[pathEndPoint]], [csvFileVicon['TX'].to_numpy()[pathEndPoint]/10], marker='*', ls='none', ms=10, color='Orange')

fig.savefig("X over time.png")

# Y over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel('y (cm)')
plt.title('Plot of Y over time')
plt.grid(True)

plt.plot(csvFileVicon['Frame'].to_numpy(), csvFileVicon['TY'].to_numpy()/10, color='Black')
plt.plot([csvFileVicon['Frame'].to_numpy()[pathStartPoint]], [csvFileVicon['TY'].to_numpy()[pathStartPoint]/10], marker='*', ls='none', ms=10, color='Purple')
plt.plot([csvFileVicon['Frame'].to_numpy()[pathEndPoint]], [csvFileVicon['TY'].to_numpy()[pathEndPoint]/10], marker='*', ls='none', ms=10, color='Orange')

fig.savefig("Y over time.png")

# Z over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel('z (cm)')
plt.title('Plot of Z over time')
plt.grid(True)

plt.plot(csvFileVicon['Frame'].to_numpy(), csvFileVicon['TZ'].to_numpy()/10, color='Black')
plt.plot(csvFileVicon['Frame'].to_numpy(), [105 for i in range(len(csvFileVicon['Frame']))], color='Green')
plt.plot([csvFileVicon['Frame'].to_numpy()[pathStartPoint]], [csvFileVicon['TZ'].to_numpy()[pathStartPoint]/10], marker='*', ls='none', ms=10, color='Purple')
plt.plot([csvFileVicon['Frame'].to_numpy()[pathEndPoint]], [csvFileVicon['TZ'].to_numpy()[pathEndPoint]/10], marker='*', ls='none', ms=10, color='Orange')

fig.savefig("Z over time.png")

# Y over X plot
fig, ax = plt.subplots()
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.title('Plot of Y over X')
plt.grid(True)

#plt.plot(csvFileVicon['TX'].to_numpy()/10, csvFileVicon['TY'].to_numpy()/10, color='Black')
#plt.plot(csvFilePathPlanner['TX'].to_numpy(), csvFilePathPlanner['TY'].to_numpy(), color='Red')
plt.plot(interpolatedViconXY[:, 0] / 10, interpolatedViconXY[:, 1] / 10, color='Blue')
plt.plot(interpolatedPathPlannerXY[:, 0], interpolatedPathPlannerXY[:, 1], color='Red')
#plt.plot([csvFileVicon['TX'].to_numpy()[0]/10], [csvFileVicon['TY'].to_numpy()[0]/10], marker='*', ls='none', ms=10, color='Green')
#plt.plot([csvFileVicon['TX'].to_numpy()[-1]/10], [csvFileVicon['TY'].to_numpy()[-1]/10], marker='*', ls='none', ms=10, color='Blue')
plt.plot([csvFileViconXYPath['TX'].to_numpy()[0]/10], [csvFileViconXYPath['TY'].to_numpy()[0]/10], marker='*', ls='none', ms=10, color='Purple')
plt.plot([csvFileViconXYPath['TX'].to_numpy()[-1]/10], [csvFileViconXYPath['TY'].to_numpy()[-1]/10], marker='*', ls='none', ms=10, color='Orange')
#plt.scatter(highErrorPoints[:, 0]/10, highErrorPoints[:, 1]/10, color='Yellow')

fig.savefig("Y over X.png")

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x (cm)')
ax.set_ylabel('y (cm)')
ax.set_zlabel('z (cm)')
ax.set_title('3D plot of path')

ax.plot(csvFileVicon['TX'].to_numpy()/10, csvFileVicon['TY'].to_numpy()/10, csvFileVicon['TZ'].to_numpy()/10, color='Black')
ax.plot(csvFilePathPlanner['TX'].to_numpy(), csvFilePathPlanner['TY'].to_numpy(), csvFilePathPlanner['TZ'].to_numpy(), color='Red')
ax.plot([csvFileVicon['TX'].to_numpy()[0]/10], [csvFileVicon['TY'].to_numpy()[0]/10], [csvFileVicon['TZ'].to_numpy()[0]/10], marker='*', ls='none', ms=10, color='Green')
ax.plot([csvFileVicon['TX'].to_numpy()[-1]/10], [csvFileVicon['TY'].to_numpy()[-1]/10], [csvFileVicon['TZ'].to_numpy()[-1]/10], marker='*', ls='none', ms=10, color='Blue')
ax.plot([csvFileViconXYPath['TX'].to_numpy()[0]/10], [csvFileViconXYPath['TY'].to_numpy()[0]/10], [csvFileViconXYPath['TZ'].to_numpy()[0]/10], marker='*', ls='none', ms=10, color='Purple')
ax.plot([csvFileViconXYPath['TX'].to_numpy()[-1]/10], [csvFileViconXYPath['TY'].to_numpy()[-1]/10], [csvFileViconXYPath['TZ'].to_numpy()[-1]/10], marker='*', ls='none', ms=10, color='Orange')

fig.savefig("3D plot.png")

plt.show()