import pygame
from scipy.spatial import ConvexHull
from scipy.interpolate import splrep , splev
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from shapely.geometry import Polygon, LineString
import numpy as np
from sympy import symbols, lambdify
from GUI.path_gen import path_generator

def length_of_trajectory(positions):
    # Calculate lengths of line segments in 3D
    lengths = [np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2) for (x1, y1, z1), (x2, y2, z2) in zip(positions[:-1], positions[1:])]

    # Add a 0 at the end of lengths because there's no next point for the last point
    lengths.append(0)

    # Update positions with lengths
    positions = [(x, y, z, length) for (x, y, z), length in zip(positions, lengths)]

    return positions

def velocity(positions):
    # Initialize the velocities
    all_xvel = [0,]
    all_yvel = [0,]
    t = [0,]  # Initialize with 0
    
    # Set the corner velocity
    corner_velocity = 20  # cm/s
    
    total_time = 0  # Initialize total_time

    for i in range(0, len(positions) - 1):
        # Calculate the distances between the points
        l1 = positions[i][3]

        # Calculate the time it takes to travel between the points
        time = l1 / corner_velocity
        total_time += time  # Add time to total_time

        # Calculate the velocities
        xvel = corner_velocity
        yvel = corner_velocity

        # Update the velocities
        all_xvel.append(xvel)
        all_yvel.append(yvel)
        #update the time
        t.append(total_time)  # Append total_time instead of time
        #print(f"Time: {total_time:.2f} s, xvel: {xvel:.2f} m/s, yvel: {yvel:.2f} m/s")

    all_xvel.append(0)
    all_yvel.append(0)
    #print(t)
    #update positions with velocities and time
    positions = [(x, y, z, xvel, yvel, l,  t) for (x, y, z, l), xvel, yvel, t in zip(positions, all_xvel, all_yvel, t)]

    return positions

def via_point_calc(pos, Vel, tf, t0, k):
    # Define the symbolic variables
    t= symbols('t')

    a0pos = pos[k]
    a1pos = Vel[k]
    a2pos = ((3/(tf*tf))*(pos[k+1]-pos[k]))-((2/tf)*Vel[k])-((1/tf)*Vel[k+1])
    a3pos = ((-2/(tf*tf*tf))*(pos[k+1]-pos[k]))+((1/(tf*tf))*(Vel[k+1]+Vel[k]))
    
    # Construct the expression for the polynomial
    poly_pos = a0pos + a1pos* (t - t0) + a2pos * (t - t0)**2 + a3pos * (t - t0)**3
    
    return poly_pos

def Cubic_polynomial_trajectory_vp(positions):
    # Initialize an empty list to store all polynomials
    all_polynomials = []

    points = 3 # Number of points to use for each polynomial

    incremental = 0

    # Process points in groups of 3
    for i in range(0, len(positions), points):
        if i == 0:
            group = positions[i:i+points]
        else:
            group = positions[i-incremental:i+points-incremental]
        incremental += 1

        # Convert the positions to a numpy array
        group = np.array(group)
        #print('Group:', group)

        # Separate the x, y, and z coordinates
        x = np.array(group[:, 0])
        y = np.array(group[:, 1])
        z = np.array(group[:, 2])
        xVel = np.array(group[:, 3])
        yVel = np.array(group[:, 4])
        t = np.array(group[:, 6])

        #print('x:', x)
        #print('y:', y)
        #print('z:', z)
        #print('t:', t) 

        for k in range(points-1):
            # Find the cubic polynomials that fit your data
            tf = t[-1]-t[0]
            t0 = 0
            t_start = t[0]
            #print('tf:', tf)

            poly_x = via_point_calc(x, xVel, tf, t_start, k)

            poly_y = via_point_calc(y, yVel, tf, t_start, k)

            poly_z = via_point_calc(z, [0 ,0 ,0], tf, t_start, k)

            print('poly_x:', poly_x)
            print('poly_y:', poly_y)
            print('poly_z:', poly_z)

            all_polynomials.append((poly_x, poly_y, poly_z, tf, t[0], t[1]))
            
    t = symbols('t')

    # Create the figure for x_values
    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('x')
    plt.title('Plot of x over time')
    plt.grid(True)

    # Loop over all polynomials
    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:
        
        # Generate a sequence of t-values
        t_values = np.linspace(0, tf, num=500)
        
        #plot the x, y and z values
        for l in range(0,len(t_values)):
            # Convert the sympy polynomial to a lambda function for easy evaluation
            func = lambdify(t, poly_x, "numpy")
            x_values = func(t_values)

            ax.plot(t_values, x_values)
        
        # Generate a sequence of t-values
        t_values = np.linspace(t0, t1, num=500) 

        # Plot x_values over t_values
        plt.plot(t_values, x_values)


    # Create the figure for x_values
    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('x')
    plt.title('Plot of x over time')
    plt.grid(True)

    # Loop over all polynomials
    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:
        
        # Generate a sequence of t-values
        t_values = np.linspace(0, tf, num=500)
        
        #plot the x, y and z values
        for l in range(0,len(t_values)):
            # Convert the sympy polynomial to a lambda function for easy evaluation
            func = lambdify(t, poly_y, "numpy")
            y_values = func(t_values)

            ax.plot(t_values, y_values)
        
        # Generate a sequence of t-values
        t_values = np.linspace(t0, t1, num=500) 

        # Plot x_values over t_values
        plt.plot(t_values, y_values)

    # Create the figure for x_values
    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('x')
    plt.title('Plot of x over time')
    plt.grid(True)

    # Loop over all polynomials
    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:
        
        # Generate a sequence of t-values
        t_values = np.linspace(0, tf, num=500)
        
        #plot the x, y and z values
        for l in range(0,len(t_values)):
            # Convert the sympy polynomial to a lambda function for easy evaluation
            func = lambdify(t, poly_z, "numpy")
            z_values = func(t_values)

            ax.plot(t_values, z_values)
        
        # Generate a sequence of t-values
        t_values = np.linspace(t0, t1, num=500) 

        # Plot x_values over t_values
        plt.plot(t_values, z_values)


    # Create a new figure for 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Loop over all polynomials
    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:
        # Generate a sequence of t-values
        t_values = np.linspace(0, tf, num=500)

        # Compute the x, y, and z values
        x_values = poly_x(t_values)
        y_values = poly_y(t_values)
        z_values = poly_z(t_values)

        # Generate a sequence of t-values
        t_values = np.linspace(t0, t1, num=500) 

        # Plot x, y, z values over t_values
        ax.plot3D(x_values, y_values, z_values)

    # Show the plot
    plt.show()
    print(all_polynomials)
    return all_polynomials

def polomial_to_points(poly_x, poly_y, poly_z, tf, t0, t1):
    t_space = 500
    t_values = np.linspace(0, tf, num=t_space)
    x_values = poly_x(t_values)
    y_values = poly_y(t_values)
    z_values = poly_z(t_values)
    t_values = np.linspace(t0, t1, num=t_space)

    zip_values = list(zip(x_values, y_values, z_values, t_values))
    return zip_values