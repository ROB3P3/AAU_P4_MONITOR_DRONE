from scipy.io import savemat

drone_path = [[0.0, 0.0, 0.0], [1.1, 2.2, 3.3], [4.4, 5.5, 6.6], [7.7, 8.8, 9.9]]

file_name = 'drone_path.mat'

savemat(file_name, {'drone_path': drone_path})