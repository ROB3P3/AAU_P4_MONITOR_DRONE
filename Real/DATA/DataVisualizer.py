from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas
import numpy as np


pathToViconCSV = "/home/drone/Documents/GitHub/AAU_P4_MONITOR_DRONE-1/Real/DATA/Crazyflie_462_Test 13.csv"
pathToPathPlannerCSV = "/home/drone/Documents/GitHub/AAU_P4_MONITOR_DRONE-1/Real/DATA/PathData.csv"

csvFileVicon = pandas.read_csv(pathToViconCSV, skiprows=[0, 1, 2, 4], usecols=['Frame', 'TX', 'TY', 'TZ'])
csvFilePathPlanner = pandas.read_csv(pathToPathPlannerCSV)

# X over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel('X')
plt.title('Plot of X over time')
plt.grid(True)

plt.plot(csvFileVicon['Frame'].to_numpy(), csvFileVicon['TX'].to_numpy()/10, color='Black')

# Y over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel('Y')
plt.title('Plot of Y over time')
plt.grid(True)

plt.plot(csvFileVicon['Frame'].to_numpy(), csvFileVicon['TY'].to_numpy()/10, color='Black')

# Z over time plot
fig, ax = plt.subplots()
plt.xlabel('Time (frames)')
plt.ylabel('Z')
plt.title('Plot of Z over time')
plt.grid(True)

plt.plot(csvFileVicon['Frame'].to_numpy(), csvFileVicon['TZ'].to_numpy()/10, color='Black')

# Y over X plot
fig, ax = plt.subplots()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Plot of Y over X')
plt.grid(True)

plt.plot(csvFileVicon['TX'].to_numpy()/10, csvFileVicon['TY'].to_numpy()/10, color='Black')
plt.plot(csvFilePathPlanner['TX'].to_numpy(), csvFilePathPlanner['TY'].to_numpy(), color='Red')
plt.plot([csvFileVicon['TX'].to_numpy()[0]/10], [csvFileVicon['TY'].to_numpy()[0]/10], marker='*', ls='none', ms=10, color='Green')
plt.plot([csvFileVicon['TX'].to_numpy()[-1]/10], [csvFileVicon['TY'].to_numpy()[-1]/10], marker='*', ls='none', ms=10, color='Blue')

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D plot of path')

ax.plot(csvFileVicon['TX'].to_numpy()/10, csvFileVicon['TY'].to_numpy()/10, csvFileVicon['TZ'].to_numpy()/10, color='Black')
ax.plot(csvFilePathPlanner['TX'].to_numpy(), csvFilePathPlanner['TY'].to_numpy(), csvFilePathPlanner['TZ'].to_numpy(), color='Red')
ax.plot([csvFileVicon['TX'].to_numpy()[0]/10], [csvFileVicon['TY'].to_numpy()[0]/10], [csvFileVicon['TZ'].to_numpy()[0]/10], marker='*', ls='none', ms=10, color='Green')
ax.plot([csvFileVicon['TX'].to_numpy()[-1]/10], [csvFileVicon['TY'].to_numpy()[-1]/10], [csvFileVicon['TZ'].to_numpy()[-1]/10], marker='*', ls='none', ms=10, color='Blue')


plt.show()