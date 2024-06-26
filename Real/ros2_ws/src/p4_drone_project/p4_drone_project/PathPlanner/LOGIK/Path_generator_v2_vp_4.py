#!/usr/bin/env python3 
# Description: This script generates a path for a robot to follow using cubic polynomials
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify
from datetime import datetime
import csv
import math
import os

def length_of_trajectory(positions):
    # Calculate lengths of line segments in 3D
    lengths = [np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2) for (x1, y1, z1), (x2, y2, z2) in zip(positions[:-1], positions[1:])]

    # Add a 0 at the end of lengths because there's no next point for the last point
    lengths.append(0)

    # Update positions with lengths
    positions = [(x, y, z, length) for (x, y, z), length in zip(positions, lengths)]

    return positions

def velocity(positions):
    # Set the corner velocity
    corner_velocity = 10  # cm/s    
    
    # Initialize the velocities
    all_xvel = [0,]
    all_yvel = [0,]
    all_zvel = [corner_velocity]
    t = [0,]  # Initialize with 0
    
    total_time = 0  # Initialize total_time

    for i in range(0, len(positions) - 1):
        # Calculate the distances between the points
        l = positions[i][3]

        # Calculate the time it takes to travel between the points
        time = l / corner_velocity
        total_time += time  # Add time to total_time

        # Calculate the velocities
        xvel = corner_velocity
        yvel = corner_velocity
        zvel = 0

        # Update the velocities
        all_xvel.append(xvel)
        all_yvel.append(yvel)
        all_zvel.append(zvel)

        #update the time
        t.append(total_time)  # Append total_time instead of time
        #print(f"Time: {total_time:.2f} s, xvel: {xvel:.2f} m/s, yvel: {yvel:.2f} m/s")

    all_xvel.append(0)
    all_yvel.append(0)
    all_zvel.append(corner_velocity)

    #update positions with velocities and time
    positions = [(x, y, z, xvel, yvel, zvel, l,  t) for (x, y, z, l), xvel, yvel, zvel, t in zip(positions, all_xvel, all_yvel, all_zvel, t)]

    return positions

def via_point_calc(pos_start, pos_slut, Vel_start, Vel_slut, tf, t0):
    # Define the symbolic variables
    t = symbols('t')

    a0pos = pos_start
    a1pos = Vel_start
    a2pos = ((3/(tf*tf))*(pos_slut-pos_start))-((2/tf)*Vel_start)-((1/tf)*Vel_slut)
    a3pos = ((-2/(tf*tf*tf))*(pos_slut-pos_start))+((1/(tf*tf))*(Vel_slut+Vel_start))
    
    # Construct the expression for the polynomial
    poly_pos = a0pos + a1pos* (t - t0) + a2pos * (t - t0)**2 + a3pos * (t - t0)**3
    
    return poly_pos

def cubicPolynomialTrajectory(positions):
    """Creates cubic polynomial equations for trajectory based on a set of positions"""
    all_polynomials = []

    for i in range(0, len(positions)-1):
        x_start, y_start, z_start, xvel_start, yvel_start, zvel_start, l, t_start = positions[i]
        #print('start position', x_start, y_start, z_start, xvel_start, yvel_start, zvel_start, l, t_start)

        x_slut, y_slut, z_slut, xvel_slut, yvel_slut, zvel_slut, l, t_slut = positions[i+1]
        #print('slut position', x_slut, y_slut, z_slut, xvel_slut, yvel_slut, zvel_slut, l, t_slut)

        t_int = t_slut - t_start
        #print('tids interval', t_int)

        poly_x = via_point_calc(x_start, x_slut, xvel_start, xvel_slut, t_int, t_start)
        poly_y = via_point_calc(y_start, y_slut, yvel_start, yvel_slut, t_int, t_start)
        #poly_z = via_point_calc(z_start, z_slut, zvel_start, zvel_slut, t_int, t_start)

        a0z = z_start
        a1z = 0
        a2z = ((3 / (t_int * t_int)) * (z_slut - z_start))
        a3z = ((-2 / (t_int * t_int * t_int)) * (z_slut - z_start))
        poly_coeffs_z = np.array([a3z, a2z, a1z, a0z])
        poly_z = np.poly1d(poly_coeffs_z, variable='t')
        
        print('poly_z', poly_z)
        
        all_polynomials.append([poly_x, poly_y, poly_z, t_int, t_start, t_slut])
    return all_polynomials
            
def plot_polynomial(all_polynomials):
    t = symbols('t')
    res_of_plot = 500

    t_values = []
    x_values = []
    y_values = []
    z_values = []

    currentDatetime = datetime.now()
    dateTimeString = str(currentDatetime.year) + "-" + str(currentDatetime.month) + "-" + str(currentDatetime.day) + "-" + str(currentDatetime.hour) + ":" + str(currentDatetime.minute)
    os.makedirs("./src/p4_drone_project/p4_drone_project/PathPlanner/DATA/" + dateTimeString + "/")
    os.chdir("./src/p4_drone_project/p4_drone_project/PathPlanner/DATA/" + dateTimeString + "/")

    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:
        # Generate a sequence of t-values
        t_temp_values = np.linspace(t0, t1, num=res_of_plot)
        t_z_temp_values = np.linspace(0, tf, num=res_of_plot)
        t_values.extend(t_temp_values)
        
        funcX = lambdify(t, poly_x, "numpy")
        funcY = lambdify(t, poly_y, "numpy")
        x_values.extend(funcX(t_temp_values))
        y_values.extend(funcY(t_temp_values))
        z_values.extend(poly_z(t_z_temp_values))
    
    fig, ax = plt.subplots()
    plt.xlabel('Time')
    plt.ylabel('x')
    plt.title('Plot of x over time')
    plt.grid(True)

    plt.plot(t_values, x_values)

    fig.savefig('X over time.png')

    # Create the figure for y_values
    fig, ax = plt.subplots()
    plt.xlabel('Time')
    plt.ylabel('y')
    plt.title('Plot of y over time')
    plt.grid(True)

    plt.plot(t_values, y_values)

    fig.savefig('Y over time.png')

    # Create the figure for z_values
    fig, ax = plt.subplots()
    plt.xlabel('Time')
    plt.ylabel('z')
    plt.title('Plot of z over time')
    plt.grid(True)

    plt.plot(t_values, z_values)

    fig.savefig('Z over time.png')
    
    # Create plot for y over x 
    fig, ax = plt.subplots()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of y over x')
    plt.grid(True)

    plt.plot(x_values, y_values)

    fig.savefig('Y over X.png')

    # Create a new figure for 3D plot
    fig = plt.figure()

    # Add a 3D subplot
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x_values, y_values, z_values)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D plot over path')
    fig.savefig('3D plot.png')

    plt.show()

    PATHPLANNER_DELTA_T = 0.5
    time_values = []
    x_points = []
    y_points = []
    z_points = []

    for poly in all_polynomials:
        for i in range(0, math.ceil(poly[3] / PATHPLANNER_DELTA_T)):
            time_values.append(poly[4] + i * PATHPLANNER_DELTA_T)
            x_points.append(poly[0].subs('t', poly[4] + i * PATHPLANNER_DELTA_T))
            y_points.append(poly[1].subs('t', poly[4] + i * PATHPLANNER_DELTA_T))
            z_points.append(np.polyval(poly[2], i * PATHPLANNER_DELTA_T))

    time_values.append(all_polynomials[-1][5])
    x_points.append(all_polynomials[-1][0].subs('t', all_polynomials[-1][5]))
    y_points.append(all_polynomials[-1][1].subs('t', all_polynomials[-1][5]))
    z_points.append(np.polyval(all_polynomials[-1][2], all_polynomials[-1][3]))

    csvDataHeader = ['Time', 'TX', 'TY', 'TZ']
    pathFileNameString = "PathData.csv"
    #pointDictArray =  convert_to_dict_points(x_values, y_values, z_values)
    pointDictArray = convert_to_dict_points(x_points, y_points, z_points, time_values)
    with open(pathFileNameString, 'a') as file:
        csvDictWriter = csv.DictWriter(file, csvDataHeader)
        file.seek(0, 2)
        if file.tell() == 0:
            csvDictWriter.writeheader()
        csvDictWriter.writerows(pointDictArray)
    
    polyFileNameString = "PolyData.csv"
    polyDictArray = convert_to_dict_poly(all_polynomials)
    with open(polyFileNameString, 'a') as file:
        csvDataHeader = ['PolyX', 'PolyY', 'PolyZ', 'Tf', 'T0', 'T1']
        csvDictWriter = csv.DictWriter(file, csvDataHeader)
        file.seek(0, 2)
        if file.tell() == 0:
            csvDictWriter.writeheader()
        csvDictWriter.writerows(polyDictArray)


def convert_to_dict_points(x_values, y_values, z_values, t_values):
    dictArray = []
    for i in range(len(x_values)):
        dictArray.append({"Time": t_values[i], "TX": x_values[i], "TY": y_values[i], "TZ": z_values[i]})
    return dictArray

def convert_to_dict_poly(polys):
    dictArray = []
    for i in range(len(polys)):
        dictArray.append({"PolyX": polys[i][0], "PolyY": polys[i][1], "PolyZ": polys[i][2], "Tf": polys[i][3], "T0": polys[i][4], "T1": polys[i][5]})
    return dictArray