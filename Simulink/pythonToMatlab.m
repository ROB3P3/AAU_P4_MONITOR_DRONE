% Load the data from the saved .mat file
loaded_data = load('drone_path.mat');

% Access the array from the loaded data
drone_path_loaded = loaded_data.drone_path;

% Get the size of the array
[row_count, ~] = size(drone_path_loaded);

% Initialize a new cell array to store the elements
y_array = {};
rows = 1;
% Loop through the rows
for i = 1:row_count
    % Initialize an empty cell array to store the elements from the current row
    row_elements = {};
    
    column = 1;
    % Loop through the columns (only columns 2 and 3)
    for j = 2:3
        % Access each element of the array
        current_element = drone_path_loaded(i, j);

        % Append the row elements cell array to the new array
        y_array{rows, column} = current_element;
        column = column+1;
    end
    % Shift to new row
    rows = rows+1;
    
end


x_array = {};
rows = 1;
% Loop through the rows
for i = 1:row_count
    % Initialize an empty cell array to store the elements from the current row
    row_elements = {};
    
    column = 1;
    % Loop through the columns (only columns 2 and 3)
    for j = [1, 3]
        % Access each element of the array
        current_element = drone_path_loaded(i, j);

        % Append the row elements cell array to the new array
        x_array{rows, column} = current_element;
        column = column+1;
    end
    
    % Shift to new row
    rows = rows+1;
end

y_array = cell2mat(y_array)
x_array = cell2mat(x_array)