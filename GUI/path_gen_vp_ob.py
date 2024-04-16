import pygame
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
import numpy as np
import math

class PathGenerator:
    def __init__(self):
        self.points = []
        self.window_size = (400, 400)
        self.point_color = (255, 0, 0)  # Red
        self.point_color2 = (1, 0, 0)  # Red
        self.point_radius = 5
        self.hull_color = (0, 255, 0)  # Green
        self.scan_color = 'blue'
        self.scan_spacing = 20  # Spacing between scan lines

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(self.window_size)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.points.append((x, y))
            screen.fill((0, 0, 0))
            for point in self.points:
                pygame.draw.circle(screen, self.point_color, point, self.point_radius)
            if len(self.points) > 2:
                hull = ConvexHull(self.points)
                for i in range(len(hull.vertices)):
                    start_point = self.points[hull.vertices[i - 1]]
                    end_point = self.points[hull.vertices[i]]
                    pygame.draw.line(screen, self.hull_color, start_point, end_point, 1)
            x, y = pygame.mouse.get_pos()
            pygame.display.set_caption(f"Mouse Position: ({x}, {y})")
            pygame.display.flip()
        pygame.quit()

    def plot(self):
        hull = ConvexHull(self.points)
        hull_polygon = Polygon([self.points[vertex] for vertex in hull.vertices])
        min_x, min_y, max_x, max_y = hull_polygon.bounds
        scan_lines = []
        for y in np.arange(min_y, max_y, self.scan_spacing):
            scan_line = LineString([(min_x, y), (max_x, y)])
            scan_lines.append(scan_line)
        intersections = [scan_line.intersection(hull_polygon) for scan_line in scan_lines]
        plt.scatter(*zip(*self.points), color=self.point_color2)
        for simplex in hull.simplices:
            plt.plot([self.points[i][0] for i in simplex], [self.points[i][1] for i in simplex], self.hull_color)
        intersection_points = []
        for intersection in intersections:
            if intersection.is_empty:
                continue
            elif intersection.geom_type == 'LineString':
                x, y = intersection.xy
                plt.plot(x, y, self.scan_color)
                intersection_points.extend(list(zip(x, y)))
            elif intersection.geom_type == 'MultiLineString':
                for line in intersection:
                    x, y = line.xy
                    plt.plot(x, y, self.scan_color)
                    intersection_points.extend(list(zip(x, y)))
        plt.gca().invert_yaxis()

if __name__ == "__main__":
    path_gen = PathGenerator()
    path_gen.run()
    path_gen.plot()
