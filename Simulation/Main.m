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
    %k = 7;
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
    % XY max error
    XYLengthList = [];
    for n = 1:numel(out.xPathError.Data)
        XYLength = sqrt(abs(out.xPathError.Data(n))^2+abs(out.yPathError.Data(n))^2);
        XYLengthList = [XYLengthList, XYLength];
    end
    maxXY = max(XYLengthList)*100;

    % Z mean and max error
    meanZ = (sum(abs(out.zPathError.Data))*100)/length(out.zPathError.Data);
    maxZ = max((abs(out.zPathError.Data)))*100;
    meanXYZ = sqrt(meanX^2+meanY^2+meanZ^2);
    
    %% Calculate Overshoot
    % find peaks in the polynomials
    xPeaks = [];
    syms t
    for n = 2:numel(PolyData(:,"PolyX"))-1
        poly = strrep(string(PolyData.PolyX(n)),"**","^");
        poly = str2sym(poly);
        Z = solve(diff(poly) == 0,  t, "Real",true);
        for j = 1:numel(Z)
            xPeaks = [xPeaks, round((Z(j)), 1)];
        end
    end
    % find the values of the peaks and the overshoot %
    overshootPercentAll = [];
    overshootAll = [];
    for n = 1:numel(xPeaks)
        if n == 1
            xRefStart = out.xPathRef.Data(find(out.xPathRef.Time == 10));
            yRefStart = out.yPathRef.Data(find(out.yPathRef.Time == 10));
            xStart = out.xPath.Data(find(out.xPath.Time == 10));
            yStart = out.yPath.Data(find(out.yPath.Time == 10));
        else
            xRefStart =out.xPathRef.Data(find(out.xPathRef.Time == xPeaks(1,n-1)));
            yRefStart = out.yPathRef.Data(find(out.yPathRef.Time == xPeaks(1,n-1)));
            xStart = out.xPath.Data(find(out.xPath.Time == xPeaks(1,n-1)));
            yStart = out.yPath.Data(find(out.yPath.Time == xPeaks(1,n-1)));
            
        end
        xRefEnd = out.xPathRef.Data(find(out.xPathRef.Time == xPeaks(1,n)));
        yRefEnd = out.yPathRef.Data(find(out.yPathRef.Time == xPeaks(1,n)));
        xEnd = out.xPath.Data(find(out.xPath.Time == xPeaks(1,n)));
        yEnd = out.yPath.Data(find(out.yPath.Time == xPeaks(1,n)));
       
        % calculate overshoot
        xInterval = abs(xEnd - xStart);
        yInterval = abs(yEnd - yStart);
        xRefInterval = abs(xRefEnd - xRefStart);
        yRefInterval = abs(yRefEnd - yRefStart);
        
        overshoot = abs(sqrt(xRefInterval^2+yRefInterval^2)-sqrt(xInterval^2+yInterval^2));
        overshootAll = [overshootAll, overshoot*100];
    
        overshootPercent = overshoot/abs(sqrt(xRefInterval^2+yRefInterval^2))*100;
        overshootPercentAll = [overshootPercentAll, overshootPercent];
    end
    % calculate mean overshoot
    meanXYOvershootPercent = sum(overshootPercentAll)/length(overshootPercentAll);
    meanXYOvershoot = sum(overshootAll)/length(overshootAll);
    
    %% export
    meanErrors = [double(test), meanX, meanY, meanXY, meanZ, meanXYZ, meanXYOvershoot, meanXYOvershootPercent, maxZ, maxXY];
    meanErrors = array2table(meanErrors, 'VariableNames', {'Test', 'meanErrorX', 'meanErrorY', 'meanErrorXY', 'meanErrorZ', 'meanErrorXYZ', 'meanXYOvershoot', 'meanXYOvershootPercent', 'maxErrorZ', 'maxErrorXY'});
    resultPath = insertAfter("DATAdir\Test \SimTestResults.csv","DATAdir\Test ", test);
    resultPath = insertBefore(resultPath,"Results.csv", test);
    writetable(meanErrors, resultPath);
    %% summarize all
    % read summary CSV
    if isfile('DATAdir\Test Results\Test Results.csv')
        % File exists.
        resultsAll = readcell('DATAdir\Test Results\Test Results.csv');
    else
        % File does not exist.
        summary = [];
        for n = 1:7
            summary = [summary; 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        end
        summary = array2table(summary, 'VariableNames', {'Test', 'meanErrorX', 'meanErrorY', 'meanErrorXY', 'meanErrorZ', 'meanErrorXYZ', 'meanXYOvershoot', 'meanXYOvershootPercent', 'maxErrorZ', 'maxErrorXY'});
        writetable(summary, 'DATAdir\Test Results\Test Results.csv');
        resultsAll = readcell('DATAdir\Test Results\Test Results.csv');
    end
    resultsAll(double(test)+1, :) = table2cell(round(meanErrors,4));
    range = insertAfter(insertAfter('A:G', 'A', test),'G',test);
    writecell(resultsAll,'DATAdir\Test Results\Test Results.csv')
    %% export Figures
    % X Y and Z figure
    xyzGraphs = get_param("Crazyflie_Simulation_Position/Position Controller/x,y,z error",'Name');
    hs = findall(0,'Name',xyzGraphs);
    % Create a new target figure
    hf = figure('Position',get(hs,'Position'));
    % Get the handle to the panel containing the plots
    hp = findobj(hs.UserData.Parent,'Tag','VisualizationPanel');
    % Copy the panel to the new figure
    copyobj(hp,hf)
    %Name = insertAfter("DATAdir\Test \xyzGraphsTest","DATAdir\Test \xyzGraphsTest", test);
    %Name = insertAfter(Name, "DATAdir\Test ", test);
    %saveas(hf, append(Name, '.fig'));
    %saveas(hf, append(Name, '.png'));
    %saveas(hf, append(Name, '.svg'));


end
