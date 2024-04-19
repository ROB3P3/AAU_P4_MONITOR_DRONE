cmake_minimum_required(VERSION 3.8)
project(my_cpp_py_pkg)

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
add_executable(cpp_executable src/cpp_node.cpp)
ament_target_dependencies(cpp_executable rclcpp std_msgs) 

add_executable(cpp_talker_node src/cpp_talker.cpp)
ament_target_dependencies(cpp_talker_node rclcpp std_msgs)

add_executable(vicon_node src/cpp_vicon.cpp)
ament_target_dependencies(vicon_node rclcpp std_msgs)

target_link_libraries(vicon_node /usr/lib/libViconDataStreamSDK_CPP.so)
target_link_libraries(cpp_executable /usr/lib/Linux64/libViconDataStreamSDK_CPP.so)
target_link_libraries(cpp_talker_node /usr/lib/libViconDataStreamSDK_CPP.so)



# Install cpp exe
install(TARGETS
  cpp_executable
  cpp_talker_node
  vicon_node
  DESTINATION lib/${PROJECT_NAME}
)


# Install Python moduels
ament_python_install_package(${PROJECT_NAME}) 

# Install Python executables
install(PROGRAMS
  scripts/py_node.py
  scripts/py_listener.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
