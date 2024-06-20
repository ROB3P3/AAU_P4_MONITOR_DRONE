%% ENSURE THAT CURRENT FOLDER IS THE ONE CONTAINING THIS FILE AND THE PROJECT FILE
% Specify python interpreter
terminate(pyenv)
pyenv
try
    pyversion("C:\Users\klump\anaconda3\envs\MonitorDrone\pythonw.exe") % insert path to python env
catch
    warning("Python interpereter already assigned");
end

% Run path planner python script
pyrunfile("Main.py")
% get parameters
Crazyflie_Param;

%% Load simulink system
model_name = "Crazyflie_Simulation_Position";
load_system(model_name);

% Automatic stop time
simIn = Simulink.SimulationInput(model_name);
%simIn = setModelParameter(simIn,"StartTime","0",...
%    "StopTime",stop_time);

% open graphs for visualisation
open_system("Crazyflie_Simulation_Position")
%open_system("Crazyflie_Simulation_Position/Position Controller/x,y,z error")
%open_system("Crazyflie_Simulation_Position/Position Controller/XY plot/XYvsRef Graph")

out = sim(simIn);


%% export Figures
if false
    % X Y and Z figure
    xyzGraphs = get_param("Crazyflie_Simulation_Position/Position Controller/x,y,z error",'Name');
    hs = findall(0,'Name',xyzGraphs);
    % Create a new target figure
    hf = figure('Position',get(hs,'Position'));
    % Get the handle to the panel containing the plots
    hp = findobj(hs.UserData.Parent,'Tag','VisualizationPanel');
    % Copy the panel to the new figure
    copyobj(hp,hf)
    Name = "DATAdir\xyzGraphsTest";
    saveas(hf, append(Name, '.fig'));
    saveas(hf, append(Name, '.png'));
    saveas(hf, append(Name, '.svg'));
end

