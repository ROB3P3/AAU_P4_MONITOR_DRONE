% Specify python interpreter
%terminate(pyenv)
%pyenv
%try
%    pyversion("C:\Users\klump\anaconda3\envs\MonitorDrone\pythonw.exe")
%catch
%    warning("Python interpereter already assigned");
%end

% Run path planner python script
%pyrunfile("Main.py")

for k = 1:7
    % get parameters
    k
    test = string(k);
    Crazyflie_Param;
    
    %% Load simulink system
    model_name = "Crazyflie_Simulation_Position";
    load_system(model_name);
    
    % Automatic stop time
    simIn = Simulink.SimulationInput(model_name);
    %simIn = setModelParameter(simIn,"StartTime","0",...
    %    "StopTime",stop_time);
    open_system("Crazyflie_Simulation_Position")
    open_system("Crazyflie_Simulation_Position/Position Controller/x,y,z error")
    open_system("Crazyflie_Simulation_Position/Position Controller/XY plot/XYvsRef Graph")
    
    out = sim(simIn);
    
    %% export values to CSV
    % export
    simPathData = [out.xPath.Time, out.xPathRef.Data, out.yPathRef.Data,out.zPathRef.Data, out.xPath.Data, out.yPath.Data,out.zPath.Data, out.xPathError.Data, out.yPathError.Data,out.zPathError.Data];
    simPathData = array2table(simPathData, 'VariableNames', {'Time', 'xPathRef', 'yPathRef', 'zPathRef', 'xPath', 'yPath', 'zPath', 'xPathError', 'yPathError', 'zPathError'});
    
    dataPath = insertAfter("DATAdir\Test \SimTestData.csv","DATAdir\Test ", test);
    dataPath = insertBefore(dataPath,"Data.csv", test);
    writetable(simPathData, dataPath);
    
    % calculate mean absolute errors
    % XY mean error ( *100 to convert to cm)
    meanX = (sum(abs(out.xPathError.Data))*100)/length(out.xPathError.Data);
    meanY = (sum(abs(out.yPathError.Data))*100)/length(out.yPathError.Data);
    meanXY = sqrt(meanX^2+meanY^2);
    % Z mean error
    meanZ = (sum(abs(out.zPathError.Data))*100)/length(out.zPathError.Data);
    meanXYZ = sqrt(meanX^2+meanY^2+meanZ^2);
    % export
    meanErrors = [meanX, meanY, meanXY, meanZ, meanXYZ];
    meanErrors = array2table(meanErrors, 'VariableNames', {'meanErrorX', 'meanErrorY', 'meanErrorXY', 'meanErrorZ', 'meanErrorXYZ'});
    resultPath = insertAfter("DATAdir\Test \SimTestResults.csv","DATAdir\Test ", test);
    resultPath = insertBefore(resultPath,"Results.csv", test);
    writetable(meanErrors, resultPath);
    
    % export Figures
    % X Y and Z figure
    xyzGraphs = get_param("Crazyflie_Simulation_Position/Position Controller/x,y,z error",'Name');
    hs = findall(0,'Name',xyzGraphs);
    % Create a new target figure
    hf = figure('Position',get(hs,'Position'));
    % Get the handle to the panel containing the plots
    hp = findobj(hs.UserData.Parent,'Tag','VisualizationPanel');
    % Copy the panel to the new figure
    copyobj(hp,hf)
    Name = insertAfter("DATAdir\Test \xyzGraphsTest","DATAdir\Test \xyzGraphsTest", test);
    Name = insertAfter(Name, "DATAdir\Test ", test);
    saveas(hf, append(Name, '.fig'));
    saveas(hf, append(Name, '.png'));
    saveas(hf, append(Name, '.svg'));


end
