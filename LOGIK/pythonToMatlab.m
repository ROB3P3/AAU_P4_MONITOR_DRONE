% Load the data from the saved .mat file
loaded_data = load('my_array.mat');

% Access the array from the loaded data
my_array_loaded = loaded_data.my_array;

% Get the size of the array
[row_count, ~] = size(my_array_loaded);

% Initialize a new cell array to store the elements
y_array = {};

% Loop through the rows
for i = 1:row_count
    % Initialize an empty cell array to store the elements from the current row
    row_elements = {};
    
    % Loop through the columns (only columns 2 and 3)
    for j = 2:3
        % Access each element of the array
        current_element = my_array_loaded(i, j);
        
        % Append the current element to the row elements cell array
        row_elements{end+1} = current_element;
    end
    
    % Append the row elements cell array to the new array
    y_array{end+1} = row_elements;
end


x_array = {};

% Loop through the rows
for i = 1:row_count
    % Initialize an empty cell array to store the elements from the current row
    row_elements = {};
    
    % Loop through the columns (only columns 2 and 3)
    for j = [1, 3]
        % Access each element of the array
        current_element = my_array_loaded(i, j);
        
        % Append the current element to the row elements cell array
        row_elements{end+1} = current_element;
    end
    
    % Append the row elements cell array to the new array
    x_array{end+1} = row_elements;
end

display(x_array{1})
display(y_array{1})
display(y_array{1}{1}+y_array{1}{1})