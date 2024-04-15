from GUI.path_gen_vp import path_generator
import LOGIK.Path_generator_v2_vp_3 as pg
import numpy as np

if __name__ == "__main__":
    positions = path_generator()
    print('Positions:', positions)
    positions =  pg.length_of_trajectory(positions)
    positions = pg.velocity(positions)
    #print('Positions:', positions)
    All_polynomials = pg.Cubic_polynomial_trajectory_vp(positions)
    #print('All_polynomials:', All_polynomials)
    pg.plot_polynomial(All_polynomials)