#!/usr/bin/env python3 
import pygame
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
import numpy as np

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
                #print(f"Added point at position: {x, y}")

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
    pattern_points = [[0, 0],]
    for i in range(0, len(intersection_points), 4):
        pattern_points.extend(intersection_points[i:i+2])
        pattern_points.extend(reversed(intersection_points[i+2:i+4]))

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
    plt.show()

    # Height of the flight path
    height = 200 #cm

    # Create an array for z
    z = np.full(len(pattern_points), height)

    # Ensure z is 0 at the first and last position
    z[0] = 0
    z[-1] = 0

    # Update positions with lengths
    pattern_points = [(x, y, z) for (x, y), z in zip(pattern_points, z)]

    return pattern_points