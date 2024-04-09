% Specify python interpreter
pyenv
try
    pyversion("C:\Users\klump\anaconda3\envs\MonitorDrone\pythonw.exe")
catch
    warning("Python interpereter already assigned");
end

% Run path planner python script
drone_path_x = pyrunfile("Path Planner.py", "all_x_values");
drone_path_y = pyrunfile("Path Planner.py", "all_y_values");
drone_path_z = pyrunfile("Path Planner.py", "all_z_values");

% get parameters
Crazyflie_Param;

% Load simulink system
model_name = "Crazyflie_Simulation_Position";
load_system(model_name);

% Automatic stop time
simIn = Simulink.SimulationInput(model_name);
simIn = setModelParameter(simIn,"StartTime","0",...
    "StopTime",stop_time);
open_system("Crazyflie_Simulation_Position/Simple Position Controller/x,y,z error")
out = sim(simIn);