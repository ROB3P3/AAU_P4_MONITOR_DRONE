import pygame
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from shapely.geometry import Polygon, LineString
from scipy.interpolate import splrep, splev
import numpy as np
from scipy.io import savemat
import os


def path_generator():
    # Initialize Pygame
    pygame.init()

    # Set the size of the window
    window_size = (400, 400)
    screen = pygame.display.set_mode(window_size)

    # Set the point properties
    point_color = (255, 0, 0)  # Red
    point_radius = 5

    # Set the hull properties
    hull_color = (0, 255, 0)  # Green

    # List to store points
    points = []

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position and add it to the points list
                x, y = pygame.mouse.get_pos()
                points.append((x, y))
                print(f"Added point at position: {x, y}")

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the points
        for point in points:
            pygame.draw.circle(screen, point_color, point, point_radius)

        # Draw the convex hull
        if len(points) > 2:
            hull = ConvexHull(points)
            for i in range(len(hull.vertices)):
                start_point = points[hull.vertices[i - 1]]
                end_point = points[hull.vertices[i]]
                pygame.draw.line(screen, hull_color, start_point, end_point, 1)

        # Display the mouse position in the window title
        x, y = pygame.mouse.get_pos()
        pygame.display.set_caption(f"Mouse Position: ({x}, {y})")

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

    # Set the point properties
    point_color = 'red'

    # Set the hull properties
    hull_color = 'green'

    # Set the scan pattern properties
    scan_color = 'blue'
    scan_spacing = 20  # Spacing between scan lines

    # Calculate the convex hull
    hull = ConvexHull(points)

    # Create a Polygon object from the hull points
    hull_polygon = Polygon([points[vertex] for vertex in hull.vertices])

    # Get the bounding box of the hull
    min_x, min_y, max_x, max_y = hull_polygon.bounds

    # Create the scan lines
    scan_lines = []
    for y in np.arange(min_y, max_y, scan_spacing):
        scan_line = LineString([(min_x, y), (max_x, y)])
        scan_lines.append(scan_line)

    # Calculate the intersections of the scan lines with the hull
    intersections = [scan_line.intersection(hull_polygon) for scan_line in scan_lines]

    # Plot the points
    plt.scatter(*zip(*points), color=point_color)

    # Plot the hull
    for simplex in hull.simplices:
        plt.plot([points[i][0] for i in simplex], [points[i][1] for i in simplex], hull_color)

    # Create a list to store intersection points
    intersection_points = []

    # Calculate the intersections of the scan lines with the hull
    intersections = [scan_line.intersection(hull_polygon) for scan_line in scan_lines]

    # Plot the scan pattern
    for intersection in intersections:
        if intersection.is_empty:
            # No intersection
            continue
        elif intersection.geom_type == 'LineString':
            # Single line segment
            x, y = intersection.xy
            plt.plot(x, y, scan_color)
            intersection_points.extend(list(zip(x, y)))  # Append intersection points
        elif intersection.geom_type == 'MultiLineString':
            # Multiple line segments
            for line in intersection:
                x, y = line.xy
                plt.plot(x, y, scan_color)
                intersection_points.extend(list(zip(x, y)))  # Append intersection points
    plt.gca().invert_yaxis()  # Invert the y-axis

    # Create a new list that follows the pattern: 1st, 2nd, 4th, 3rd, 5th, 6th, ...
    pattern_points = [[0, 0], ]
    for i in range(0, len(intersection_points), 4):
        pattern_points.extend(intersection_points[i:i + 2])
        pattern_points.extend(reversed(intersection_points[i + 2:i + 4]))

    # Add the first and last point at the beginning and end to repeat them
    pattern_points.insert(0, pattern_points[0])  # Repeat the first point at the beginning

    # Add the first point at the end to close the loop
    pattern_points.append(pattern_points[1])
    pattern_points.append(pattern_points[1])

    # Plot the points following the pattern
    plt.figure()
    plt.plot(*zip(*pattern_points), 'b-')  # 'b-' means blue color and solid line
    plt.scatter(*zip(*intersection_points), color='red')  # Plot the original points in red
    plt.gca().invert_yaxis()  # Invert the y-axis
    #plt.show()

    # Height of the flight path
    height = 100  # cm

    # Create an array for z
    z = np.full(len(pattern_points), height)

    # Ensure z is 0 at the first and last position
    z[0] = 0
    z[-1] = 0

    # Update positions with lengths
    pattern_points = [(x, y, z) for (x, y), z in zip(pattern_points, z)]

    return pattern_points


def length_of_trajectory(positions):
    # Calculate lengths of line segments in 3D
    lengths = [np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) for (x1, y1, z1), (x2, y2, z2) in
               zip(positions[:-1], positions[1:])]

    # Add a 0 at the end of lengths because there's no next point for the last point
    lengths.append(0)

    # Update positions with lengths
    positions = [(x, y, z, length) for (x, y, z), length in zip(positions, lengths)]

    return positions


def velocity(positions):
    # Initialize the velocities
    all_xvel = [0, ]
    all_yvel = [0, ]
    t = [0, ]  # Initialize with 0

    # Set the corner velocity
    corner_velocity = 40  # cm/s

    total_time = 0  # Initialize total_time

    for i in range(0, len(positions) - 1):
        # Calculate the distances between the points
        x1, y1, z1, l1 = positions[i]

        # Calculate the time it takes to travel between the points
        time = l1 / corner_velocity
        total_time += time  # Add time to total_time

        # Calculate the velocities
        xvel = corner_velocity
        yvel = corner_velocity

        # Update the velocities
        all_xvel.append(xvel)
        all_yvel.append(yvel)
        # update the time
        t.append(total_time)  # Append total_time instead of time
        # print(f"Time: {total_time:.2f} s, xvel: {xvel:.2f} m/s, yvel: {yvel:.2f} m/s")

    all_xvel.append(0)
    all_yvel.append(0)
    print('Total time:', t)
    # update positions with velocities and time
    positions = [(x, y, z, xvel, yvel, l, t) for (x, y, z, l), xvel, yvel, t in zip(positions, all_xvel, all_yvel, t)]

    return positions


def Cubic_polynomial_trajectory_no_vp(positions):
    # Initialize an empty list to store all polynomials
    all_polynomials = []

    points = 2  # Number of points to use for each polynomial
    # Process points in groups of 2
    for i in range(0, len(positions)):
        group = positions[i:i + points]

        # Convert the positions to a numpy array
        group = np.array(group)
        # print('Group:', group)

        # Separate the x, y, and z coordinates
        x = np.array(group[:, 0])
        y = np.array(group[:, 1])
        z = np.array(group[:, 2])
        t = np.array(group[:, 6])
        # print('x:', x)
        # print('y:', y)
        # print('z:', z)
        # print('t:', t)

        for k in range(len(x) - 1):
            # Find the cubic polynomials that fit your data
            tf = t[-1] - t[0]
            t0 = 0
            # print('tf:', tf)

            a0x = x[k]
            a1x = 0
            a2x = ((3 / (tf * tf)) * (x[k + 1] - x[k]))
            a3x = ((-2 / (tf * tf * tf)) * (x[k + 1] - x[k]))
            poly_coeffs_x = np.array([a3x, a2x, a1x, a0x])
            poly_x = np.poly1d(poly_coeffs_x, variable='t')

            a0y = y[k]
            a1y = 0
            a2y = ((3 / (tf * tf)) * (y[k + 1] - y[k]))
            a3y = ((-2 / (tf * tf * tf)) * (y[k + 1] - y[k]))
            poly_coeffs_y = np.array([a3y, a2y, a1y, a0y])
            poly_y = np.poly1d(poly_coeffs_y, variable='t')

            a0z = z[k]
            a1z = 0
            a2z = ((3 / (tf * tf)) * (z[k + 1] - z[k]))
            a3z = ((-2 / (tf * tf * tf)) * (z[k + 1] - z[k]))
            poly_coeffs_z = np.array([a3z, a2z, a1z, a0z])
            poly_z = np.poly1d(poly_coeffs_z, variable='t')

            # print('poly_x:', poly_x)
            # print('poly_y:', poly_y)
            # print('poly_z:', poly_z)

            all_polynomials.append((poly_x, poly_y, poly_z, tf, t[0], t[1]))

            # Generate a sequence of t-values
            t_values = np.linspace(t0, tf, num=500)
            # plot the x, y and z values
            x_values = poly_x(t_values)
            y_values = poly_y(t_values)

            t_values = np.linspace(t[0], t[1], num=500)

    # Create the figure for x_values
    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('x')
    plt.title('Plot of x over time')
    plt.grid(True)

    all_x_values = []
    all_tx_values = []
    # Loop over all polynomials
    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:
        # Generate a sequence of t-values
        t_values = np.linspace(0, tf, num=500)
        # Compute the x_values
        x_values = poly_x(t_values)
        # Generate a sequence of t-values
        t_values = np.linspace(t0, t1, num=500)

        # Plot x_values over t_values
        plt.plot(t_values, x_values)

        # combine all x_values into one array
        all_x_values.extend(x_values)
        all_tx_values.extend(t_values)

    # Combine all x_values and t_values into one vertical array
    all_x_points = []
    for i in range(len(all_x_values)):
        all_x_points.append([all_tx_values[i], all_x_values[i] / 100])

    # Save the x_values to a .mat file
    # change OS to DATAdir directory
    os.chdir('..')
    os.chdir('DATAdir')
    file_name = 'drone_path_x.mat'
    savemat(file_name, {'drone_path_x': all_x_points})

    # Create the figure for y_values
    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('y')
    plt.title('Plot of y over time')
    plt.grid(True)

    all_y_values = []
    all_ty_values = []
    # Loop over all polynomials
    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:
        # Generate a sequence of t-values
        t_values = np.linspace(0, tf, num=500)
        # Compute the y_values
        y_values = poly_y(t_values)
        # Generate a sequence of t-values
        t_values = np.linspace(t0, t1, num=500)

        # Plot y_values over t_values
        plt.plot(t_values, y_values)

        all_y_values.extend(y_values)
        all_ty_values.extend(t_values)
    # Combine all x_values and t_values into one vertical array
    all_y_points = []
    for i in range(len(all_y_values)):
        all_y_points.append([all_ty_values[i], all_y_values[i] / 100])

    # Save the x_values to a .mat file
    file_name = 'drone_path_y.mat'
    savemat(file_name, {'drone_path_y': all_y_points})

    # Create the figure for z_values
    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('z')
    plt.title('Plot of z over time')
    plt.grid(True)

    all_z_values = []
    all_tz_values = []

    # Loop over all polynomials
    for poly_x, poly_y, poly_z, tf, t0, t1 in all_polynomials:
        # Generate a sequence of t-values
        t_values = np.linspace(0, tf, num=500)
        # Compute the z_values
        z_values = poly_z(t_values)
        # Generate a sequence of t-values
        t_values = np.linspace(t0, t1, num=500)

        # Plot z_values over t_values
        plt.plot(t_values, z_values)

        all_z_values.extend(z_values)
        all_tz_values.extend(t_values)

    # Combine all x_values and t_values into one vertical array
    all_z_points = []
    for i in range(len(all_z_values)):
        all_z_points.append([all_tz_values[i], all_z_values[i] / 100])

    # Save the x_values to a .mat file
    file_name = 'drone_path_z.mat'
    savemat(file_name, {'drone_path_z': all_z_points})

    # Show the plot
    #plt.show()
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
    #plt.show()
    # print(all_polynomials)
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


if __name__ == "__main__":
    positions = path_generator()
    positions = length_of_trajectory(positions)
    print('Positions:', positions)
    positions = velocity(positions)
    poly_x, poly_y, poly_z, tf, t0, t1 = Cubic_polynomial_trajectory_no_vp(np.array(positions))[0]
    zip_values = polomial_to_points(poly_x, poly_y, poly_z, tf, t0, t1)
    # print(zip_values)