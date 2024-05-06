from GUI.path_gen_vp_2 import path_generator
import LOGIK.Path_generator_v2_vp_4_Final as pg
import numpy as np

if __name__ == "__main__":
    scan_pattern = path_generator()
    #print('scan_pattern:', scan_pattern)
    positions =  pg.length_of_trajectory(scan_pattern)
    positions = pg.velocity(positions)
    #print('Positions:', positions)
    All_polynomials = pg.Cubic_polynomial_trajectory_vp(positions)
    #print('All_polynomials:', All_polynomials)
    pg.plot_polynomial(All_polynomials)