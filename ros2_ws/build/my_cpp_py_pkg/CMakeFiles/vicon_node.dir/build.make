# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/src/my_cpp_py_pkg

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/build/my_cpp_py_pkg

# Include any dependencies generated for this target.
include CMakeFiles/vicon_node.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/vicon_node.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/vicon_node.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/vicon_node.dir/flags.make

CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.o: CMakeFiles/vicon_node.dir/flags.make
CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.o: /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/src/my_cpp_py_pkg/src/cpp_vicon.cpp
CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.o: CMakeFiles/vicon_node.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/build/my_cpp_py_pkg/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.o -MF CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.o.d -o CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.o -c /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/src/my_cpp_py_pkg/src/cpp_vicon.cpp

CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/src/my_cpp_py_pkg/src/cpp_vicon.cpp > CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.i

CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/src/my_cpp_py_pkg/src/cpp_vicon.cpp -o CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.s

# Object files for target vicon_node
vicon_node_OBJECTS = \
"CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.o"

# External object files for target vicon_node
vicon_node_EXTERNAL_OBJECTS =

vicon_node: CMakeFiles/vicon_node.dir/src/cpp_vicon.cpp.o
vicon_node: CMakeFiles/vicon_node.dir/build.make
vicon_node: /opt/ros/humble/lib/librclcpp.so
vicon_node: /opt/ros/humble/lib/libstd_msgs__rosidl_typesupport_fastrtps_c.so
vicon_node: /opt/ros/humble/lib/libstd_msgs__rosidl_typesupport_fastrtps_cpp.so
vicon_node: /opt/ros/humble/lib/libstd_msgs__rosidl_typesupport_introspection_c.so
vicon_node: /opt/ros/humble/lib/libstd_msgs__rosidl_typesupport_introspection_cpp.so
vicon_node: /opt/ros/humble/lib/libstd_msgs__rosidl_typesupport_cpp.so
vicon_node: /opt/ros/humble/lib/libstd_msgs__rosidl_generator_py.so
vicon_node: /usr/lib/libViconDataStreamSDK_CPP.so
vicon_node: /opt/ros/humble/lib/liblibstatistics_collector.so
vicon_node: /opt/ros/humble/lib/librcl.so
vicon_node: /opt/ros/humble/lib/librmw_implementation.so
vicon_node: /opt/ros/humble/lib/libament_index_cpp.so
vicon_node: /opt/ros/humble/lib/librcl_logging_spdlog.so
vicon_node: /opt/ros/humble/lib/librcl_logging_interface.so
vicon_node: /opt/ros/humble/lib/librcl_interfaces__rosidl_typesupport_fastrtps_c.so
vicon_node: /opt/ros/humble/lib/librcl_interfaces__rosidl_typesupport_introspection_c.so
vicon_node: /opt/ros/humble/lib/librcl_interfaces__rosidl_typesupport_fastrtps_cpp.so
vicon_node: /opt/ros/humble/lib/librcl_interfaces__rosidl_typesupport_introspection_cpp.so
vicon_node: /opt/ros/humble/lib/librcl_interfaces__rosidl_typesupport_cpp.so
vicon_node: /opt/ros/humble/lib/librcl_interfaces__rosidl_generator_py.so
vicon_node: /opt/ros/humble/lib/librcl_interfaces__rosidl_typesupport_c.so
vicon_node: /opt/ros/humble/lib/librcl_interfaces__rosidl_generator_c.so
vicon_node: /opt/ros/humble/lib/librcl_yaml_param_parser.so
vicon_node: /opt/ros/humble/lib/libyaml.so
vicon_node: /opt/ros/humble/lib/librosgraph_msgs__rosidl_typesupport_fastrtps_c.so
vicon_node: /opt/ros/humble/lib/librosgraph_msgs__rosidl_typesupport_fastrtps_cpp.so
vicon_node: /opt/ros/humble/lib/librosgraph_msgs__rosidl_typesupport_introspection_c.so
vicon_node: /opt/ros/humble/lib/librosgraph_msgs__rosidl_typesupport_introspection_cpp.so
vicon_node: /opt/ros/humble/lib/librosgraph_msgs__rosidl_typesupport_cpp.so
vicon_node: /opt/ros/humble/lib/librosgraph_msgs__rosidl_generator_py.so
vicon_node: /opt/ros/humble/lib/librosgraph_msgs__rosidl_typesupport_c.so
vicon_node: /opt/ros/humble/lib/librosgraph_msgs__rosidl_generator_c.so
vicon_node: /opt/ros/humble/lib/libstatistics_msgs__rosidl_typesupport_fastrtps_c.so
vicon_node: /opt/ros/humble/lib/libstatistics_msgs__rosidl_typesupport_fastrtps_cpp.so
vicon_node: /opt/ros/humble/lib/libstatistics_msgs__rosidl_typesupport_introspection_c.so
vicon_node: /opt/ros/humble/lib/libstatistics_msgs__rosidl_typesupport_introspection_cpp.so
vicon_node: /opt/ros/humble/lib/libstatistics_msgs__rosidl_typesupport_cpp.so
vicon_node: /opt/ros/humble/lib/libstatistics_msgs__rosidl_generator_py.so
vicon_node: /opt/ros/humble/lib/libstatistics_msgs__rosidl_typesupport_c.so
vicon_node: /opt/ros/humble/lib/libstatistics_msgs__rosidl_generator_c.so
vicon_node: /opt/ros/humble/lib/libtracetools.so
vicon_node: /opt/ros/humble/lib/libbuiltin_interfaces__rosidl_typesupport_fastrtps_c.so
vicon_node: /opt/ros/humble/lib/librosidl_typesupport_fastrtps_c.so
vicon_node: /opt/ros/humble/lib/libbuiltin_interfaces__rosidl_typesupport_fastrtps_cpp.so
vicon_node: /opt/ros/humble/lib/librosidl_typesupport_fastrtps_cpp.so
vicon_node: /opt/ros/humble/lib/libfastcdr.so.1.0.24
vicon_node: /opt/ros/humble/lib/librmw.so
vicon_node: /opt/ros/humble/lib/libbuiltin_interfaces__rosidl_typesupport_introspection_c.so
vicon_node: /opt/ros/humble/lib/libbuiltin_interfaces__rosidl_typesupport_introspection_cpp.so
vicon_node: /opt/ros/humble/lib/librosidl_typesupport_introspection_cpp.so
vicon_node: /opt/ros/humble/lib/librosidl_typesupport_introspection_c.so
vicon_node: /opt/ros/humble/lib/libbuiltin_interfaces__rosidl_typesupport_cpp.so
vicon_node: /opt/ros/humble/lib/librosidl_typesupport_cpp.so
vicon_node: /opt/ros/humble/lib/libstd_msgs__rosidl_typesupport_c.so
vicon_node: /opt/ros/humble/lib/libstd_msgs__rosidl_generator_c.so
vicon_node: /opt/ros/humble/lib/libbuiltin_interfaces__rosidl_generator_py.so
vicon_node: /opt/ros/humble/lib/libbuiltin_interfaces__rosidl_typesupport_c.so
vicon_node: /opt/ros/humble/lib/libbuiltin_interfaces__rosidl_generator_c.so
vicon_node: /opt/ros/humble/lib/librosidl_typesupport_c.so
vicon_node: /opt/ros/humble/lib/librcpputils.so
vicon_node: /opt/ros/humble/lib/librosidl_runtime_c.so
vicon_node: /opt/ros/humble/lib/librcutils.so
vicon_node: /usr/lib/x86_64-linux-gnu/libpython3.10.so
vicon_node: CMakeFiles/vicon_node.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/build/my_cpp_py_pkg/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable vicon_node"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/vicon_node.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/vicon_node.dir/build: vicon_node
.PHONY : CMakeFiles/vicon_node.dir/build

CMakeFiles/vicon_node.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/vicon_node.dir/cmake_clean.cmake
.PHONY : CMakeFiles/vicon_node.dir/clean

CMakeFiles/vicon_node.dir/depend:
	cd /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/build/my_cpp_py_pkg && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/src/my_cpp_py_pkg /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/src/my_cpp_py_pkg /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/build/my_cpp_py_pkg /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/build/my_cpp_py_pkg /home/frederik/Documents/P4/P4Git/AAU_P4_MONITOR_DRONE/ros2_ws/build/my_cpp_py_pkg/CMakeFiles/vicon_node.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/vicon_node.dir/depend

