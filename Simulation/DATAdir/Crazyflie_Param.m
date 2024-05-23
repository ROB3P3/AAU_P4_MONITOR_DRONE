% --- crazyflie parameters
g = 9.816; % Gravity constant in DK
%g = 9.8067; %old

l1 = 4.65; %cm  1/2 of length of body
l2 = 4.5; %cm length of propeller


%Rotor/Propeller parameters
m = 0.0003; %propellor mass  kg
%m = 0.0002; %old
J = 1/12*m*(0.1^2+0.01^2); %moment of inertia from mass, kgm^2
b = 3.5077E-10; %motor viscous friction constant Nms


%drone parameters
m_drone = 0.03;   % kg
%m_drone = 0.03097;   %old kg
Ix_drone = 1.395*10^-5;  % kg*m^2
Iy_drone = 1.436*10^-5;  % kg*m^2
Iz_drone = 2.173*10^-5;  % kg*m^2
%Ix_drone = 1.112951*10^-5;  %old kg*m^2
%Iy_drone = 1.1143608*10^-5;  %old kg*m^2
%Iz_drone = 2.162056*10^-5;  %old kg*m^2
b_drone = 1*10^-9; % kg*m^2 drone's x,y,z translational drag coefficient

% Path coordinates
%load("drone_path_x.mat")
%load("drone_path_y.mat")
%load("drone_path_z.mat")
%load("drone_path.mat")
PathData = readtable(insertAfter("DATAdir\Test \PathData.csv","DATAdir\Test ", test));
PolyData = readtable(insertAfter("DATAdir\Test \PolyData.csv","DATAdir\Test ", test));
drone_path_x = PathData{:,["Time", "TX"]};
drone_path_x(:,2) = drone_path_x(:,2) .* 0.01;
drone_path_y = PathData{:,["Time", "TY"]};
drone_path_y(:,2) = drone_path_y(:,2) .* 0.01;

zMode = 1;
if zMode == 1 % 10cm/s normal
    drone_path_z = PathData{:,["Time", "TZ"]};
    drone_path_z(:,2) = drone_path_z(:,2) .* 0.01;
    % Get the last time
    stop_time = string(drone_path_z(end,1));
elseif zMode == 2 % twice as fast 20cm/s
    drone_path_z = PathData{:,["Time", "TZ"]};
    drone_path_z(:,2) = drone_path_z(:,2) .* 0.01;
    drone_path_z(:,1) = drone_path_z(:,1) .* 0.5;
    % Get the last time
    stop_time = string(drone_path_z(end,1));
elseif zMode == 3 % five as fast 50cm/s
    drone_path_z = PathData{:,["Time", "TZ"]};
    drone_path_z(:,2) = drone_path_z(:,2) .* 0.01;
    drone_path_z(:,1) = drone_path_z(:,1) .* 0.2;
    % Get the last time
    stop_time = string(drone_path_z(end,1));
elseif zMode == 4 % swerve z path
    drone_path_z = PathData{:,["Time", "TZ"]};
    drone_path_z(:,2) = drone_path_z(:,2) .* 0.01;
    
    % Get the last time
    stop_time = string(drone_path_z(end,1));

    stop_time_z = length(drone_path_z(:,1)) - 20;
    
    % merge with y path to make swerve
    drone_path_z(22:stop_time_z,2) = drone_path_z(22:stop_time_z,2) + drone_path_y(22:stop_time_z,2);
elseif zMode == 5
    

    drone_path_z = PathData{:,["Time", "TZ"]};
    drone_path_z(:,2) = drone_path_z(:,2) .* 0.01;
    drone_path_z(:,2) = drone_path_z(:,2) .* zAlt;
    % Get the last time
    stop_time = string(drone_path_z(end,1));
    zAlt = zAlt + 0.1;
end

