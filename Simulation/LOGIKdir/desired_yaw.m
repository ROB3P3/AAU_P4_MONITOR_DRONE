% get desired yaw
drone_path_yaw = drone_path_x;
for k = 1:size(drone_path_x, 1)
    % take desired x and y vector and compare to previous x and y vector to
    % find desired yaw
    currentXY = [drone_path_x(k, 2), drone_path_y(k, 2)];
    % for first vector assume previous XY was 0, 0
    if k >= 2
        previousXY = [drone_path_x(k-1, 2), drone_path_y(k-1, 2)];
    else
        previousXY = [0, 0];
    end
    desiredYaw = atan2d(currentXY(1)*previousXY(2)-currentXY(2)*previousXY(1), currentXY(1)*previousXY(1)+currentXY(2)*previousXY(2))
    drone_path_yaw(k, 2) = desiredYaw;
end