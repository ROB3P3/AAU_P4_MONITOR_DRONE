from GUI.path_gen import path_generator
import LOGIK.Path_generator_v2_vp_2 as pg
import numpy as np

if __name__ == "__main__":
    positions = path_generator()
    print('Positions:', positions)
    positions =  pg.length_of_trajectory(positions)
    positions = pg.velocity(positions)
    poly_x, poly_y, poly_z, tf, t0, t1 = pg.Cubic_polynomial_trajectory_vp(np.array(positions))[0]
    zip_values = pg.polomial_to_points(poly_x, poly_y, poly_z, tf, t0, t1)
    #print(zip_values)