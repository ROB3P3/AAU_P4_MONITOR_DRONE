from scipy.io import savemat

drone_path = [[0.0, 0.0, 0.0], [0.0, 0.0, 4], [1, 0, 1+10/2], [1, 1, 1+15/2], [2, 1, 1+20/2], [2, 0, 1+25/2], [3, 0, 1+30/2], [3, 1, 1+35/2],[3, 1, 1+40/2], [0, 0, 30],[0, 0, 40]]

file_name = 'drone_path.mat'

savemat(file_name, {'drone_path': drone_path})