from GUIdir.GUI import path_generator
import LOGIKdir.Path_generator as pg
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