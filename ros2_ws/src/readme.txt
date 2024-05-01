Du skal kalde colcon build ude fra ros2pycpp_ws mappen. 
Det kan godt ske at man skal huske at slætte det tidligere build så man kan har "src" mappen til at ligge. 
Hvis systemet forvolder problermer med at bygge skal man gen "soarce" sin konsol 
jeg har lagt et scrips som hedder ros_source.bashrc som ligger i "home" mappen, den indeholder en sti til "setup.bash" filen
så man ikke selv skal skrive den ind hver gang. Denne fil indeholder følgende:
source /home/frederik/ros2pycpp_ws/install/setup.bash


yder mere har jeg tiføjet følgende til min .bashrc fil:
source /opt/ros/humble/setup.bash
source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash
source ~/Documents/P4/AAU_P4_MONITOR_DRONE/ros2_ws/install/setup.bash

Husk at du nu skal "linke" til nogle .so filer, dette kan formodentligt gøres i Cmake. du kan se hvilke filer der skal linkes i dokunentationen.

du skal lægge alle dine .so filer i din usr/lib mappe. 
