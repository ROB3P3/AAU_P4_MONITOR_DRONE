# Description: This script generates a path for a robot to follow using cubic polynomials

import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify

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
        l1 = positions[i][3]

        # Calculate the time it takes to travel between the points
        time = l1 / corner_velocity
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

def Cubic_polynomial_trajectory_vp(positions):
    
    all_polynomials = []

    for i in range(0, len(positions)-1):
        x_start, y_start, z_start, xvel_start, yvel_start, zvel_start, l, t_start = positions[i]
        print('start position', x_start, y_start, z_start, xvel_start, yvel_start, zvel_start, l, t_start)

        x_slut, y_slut, z_slut, xvel_slut, yvel_slut, zvel_slut, l, t_slut = positions[i+1]
        print('slut position', x_slut, y_slut, z_slut, xvel_slut, yvel_slut, zvel_slut, l, t_slut)

        t_int = t_slut - t_start
        print('tids interval', t_int)

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
        
        all_polynomials.append((poly_x, poly_y, poly_z, t_int, t_start, t_slut))
    return all_polynomials
            
def plot_polynomial(all_polynomials):
    t = symbols('t')

    # Create the figure for x_values
    fig, ax = plt.subplots()
    plt.xlabel('Time')
    plt.ylabel('x')
    plt.title('Plot of x over time')
    plt.grid(True)

    # Loop over all polynomials
    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:
        
        # Generate a sequence of t-values
        t_values = np.linspace(t0, t1, num=500) 
        
        #plot the x, y and z values
        for l in range(0,len(t_values)):
            # Convert the sympy polynomial to a lambda function for easy evaluation
            func = lambdify(t, poly_x, "numpy")
            x_values = func(t_values)

            ax.plot(t_values, x_values)

        # Plot x_values over t_values
        plt.plot(t_values, x_values)
    

    # Create the figure for y_values
    fig, ax = plt.subplots()
    plt.xlabel('Time')
    plt.ylabel('y')
    plt.title('Plot of y over time')
    plt.grid(True)

    # Loop over all polynomials
    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:
        
        # Generate a sequence of t-values
        t_values = np.linspace(t0, t1, num=500)
        
        #plot the x, y and z values
        for l in range(0,len(t_values)):
            # Convert the sympy polynomial to a lambda function for easy evaluation
            func = lambdify(t, poly_y, "numpy")
            y_values = func(t_values)

            ax.plot(t_values, y_values)

        # Plot y_values over t_values
        plt.plot(t_values, y_values)

    # Create the figure for z_values
    fig, ax = plt.subplots()
    plt.xlabel('Time')
    plt.ylabel('z')
    plt.title('Plot of z over time')
    plt.grid(True)

    # Loop over all polynomials
    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:
        
        # Generate a sequence of t-values
        t_values = np.linspace(t0, t1, num=500)
        
        #plot the x, y and z values
        for l in range(0,len(t_values)):
            # Convert the sympy polynomial to a lambda function for easy evaluation
            poly_z = lambdify(t, poly_z, "numpy")
            z_values = poly_z(t_values)
            print('z_values', z_values)

            ax.plot(t_values, z_values)

        # Plot y_values over t_values
        plt.plot(t_values, z_values)
    plt.show()

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of y over x')
    plt.grid(True)

    # Loop over all polynomials
    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:

        # Generate a sequence of t-values
        t_values = np.linspace(t0, t1, num=500)

        # Convert the sympy polynomial to a lambda function for easy evaluation
        func_x = lambdify(t, poly_x, "numpy")
        func_y = lambdify(t, poly_y, "numpy")

        # Compute x and y values
        x_values = func_x(t_values)
        y_values = func_y(t_values)

        # Plot x_values and y_values
        plt.plot(x_values, y_values)

    plt.gca().invert_yaxis()
    plt.show()

    return x_values, y_values

def polomial_to_points(x_values, y_values, z_values, tf, t0, t1):
    t_space = 500
    t_values = np.linspace(0, tf, num=t_space)
    t_values = np.linspace(t0, t1, num=t_space)
    zip_values = list(zip(x_values, y_values, z_values, t_values))
    return zip_values