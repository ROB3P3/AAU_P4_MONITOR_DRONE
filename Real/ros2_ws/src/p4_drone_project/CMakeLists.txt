cmake_minimum_required(VERSION 3.8)
project(p4_drone_project)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)


# Include cpp "include" dir
include_directories(include)

#find_library(MYLIB libViconDataStreamSDK_CPP.so)

# Create cpp exe
add_executable(vicon_node src/cpp_vicon.cpp)
ament_target_dependencies(vicon_node rclcpp std_msgs)

target_link_libraries(vicon_node /home/drone/ViconLib/ViconDataStreamSDK_1.12_145507h/20230413_145507h/Release/Linux64/libViconDataStreamSDK_CPP.so)

# Install cpp exe
install(TARGETS
  vicon_node
  DESTINATION lib/${PROJECT_NAME}
)


# Install Python moduels
ament_python_install_package(${PROJECT_NAME}) 

# Install Python executables
install(PROGRAMS
  scripts/regulator_node.py
  scripts/motion_controller_node.py
  scripts/path_planner_node.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
