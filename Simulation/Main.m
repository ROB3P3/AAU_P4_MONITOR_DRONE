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
testStart = 1;
testSlut = 11;
zAlt = 0.5;
for k = testStart:testSlut
    % get parameters
    %k = 4;
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
    %open_system("Crazyflie_Simulation_Position/Position Controller/XY plot/XYvsRef Graph")
    
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
    meanX = (sum(abs(out.xPathError.Data(200:300)))*100)/length(out.xPathError.Data(200:300));
    meanY = (sum(abs(out.yPathError.Data(200:300)))*100)/length(out.yPathError.Data(200:300));
    meanXY = sqrt(meanX^2+meanY^2);
    % XY max error
    XYLengthList = [];
    %for n = 1:numel(out.xPathError.Data)
    for n = 200:300
        XYLength = sqrt(abs(out.xPathError.Data(n))^2+abs(out.yPathError.Data(n))^2);
        XYLengthList = [XYLengthList, XYLength];
    end
    maxXY = max(XYLengthList)*100;

    %% XYZ mean and max error
    meanZ = (sum(abs(out.zPathError.Data(200:300)))*100)/length(out.zPathError.Data(200:300));
    maxZ = max((abs(out.zPathError.Data(200:300))))*100;
    meanXYZ = sqrt(meanX^2+meanY^2+meanZ^2);
    % XY max error
    XYZLengthList = [];
    for n = 200:300
        XYZLength = sqrt(abs(out.xPathError.Data(n))^2+abs(out.yPathError.Data(n))^2+abs(out.zPathError.Data(n))^2);
        XYZLengthList = [XYZLengthList, XYZLength];
    end
    maxXYZ = max(XYZLengthList)*100;

    %% XY velocity mean and max error
    meanDX = (sum(abs(out.dxPathError.Data(100:end-100,1)))*100)/length(out.dxPathError.Data(100:end-100,1));
    meanDY = (sum(abs(out.dyPathError.Data(100:end-100,1)))*100)/length(out.dyPathError.Data(100:end-100,1));
    meanDXY = sqrt(meanDX^2+meanDY^2);
    % dXY max error
    dXYLengthList = [];
    DXYlist = [];
    for n = 100:numel(out.dxPathError.Data)-100
        DX = abs(out.dxPathError.Data(n))*100;
        DY = abs(out.dyPathError.Data(n))*100;
        DXY = sqrt(DX^2+DY^2);
        dXYLengthList = [dXYLengthList, DXY];
    end
    maxDXY = max(dXYLengthList)
    
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
    if false
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
    end
    %% export
    meanErrors = [double(test), meanXY, meanXYZ, meanZ, maxZ, maxXY, maxXYZ, meanDXY, maxDXY];
    meanErrors = array2table(meanErrors, 'VariableNames', {'Test', 'Mean XY Error','Mean XYZ Error', 'Mean Z Error', 'Max Z Error', 'Max XY Error','Max XYZ Error', 'Mean dXY Error', 'Max dXY Error'});
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
        for n = 1:13
            summary = [summary; 0, 0, 0, 0, 0, 0, 0, 0, 0];
        end
        summary = array2table(summary, 'VariableNames', {'Test', 'Mean XY Error','Mean XYZ Error', 'Mean Z Error', 'Max Z Error', 'Max XY Error','Max XYZ Error', 'Mean dXY Error', 'Max dXY Error'});
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
    Name = insertAfter("DATAdir\Test \xyzGraphsTest","DATAdir\Test \xyzGraphsTest", test);
    Name = insertAfter(Name, "DATAdir\Test ", test);
    saveas(hf, append(Name, '.fig'));
    saveas(hf, append(Name, '.png'));
    saveas(hf, append(Name, '.svg'));
    
end
