# AAU ROB4 Monitor drone project.
For at bygge ROS workspacet skal colcon build kaldes ude fra ros2_ws mappen.
Hvis man vil bygge det fra bunden skal alle mapper undtagen src slettes inden colcon build kaldes.
Efter den er bygget skal setup.bash filen sources fra ros2_ws/install mappen.
Hvis man er inde i ros2_ws mappen så:
source ./install/setup.bash

Og hvis man vil bygge den ind i .bashrc så den bliver sourcet automatisk ved åbning af en terminal så:
1. Først åben .bashrc filen 'nano ~/.bashrc'
2. Scroll ned til hvor der står de forskellige 'source' kommandoer
3. Tilføj filstien til den tidligere setup.bash
4. Gem .bashrc filen

ROS filerne kan derefter kaldes ved:
ros2 run p4_drone_project <navn på node>

## Library requirements til Python filer i ROS systemet:
### Python 3.11,
Pygame (pip install via anaconda prompt, the rest can be installed via anaconda navigator),
shapely,
scipy,
matplotlib,
numpy

### Simulink & Matlab:
Matlab 2024a,
Aerospace Blockset,
Aerospace Toolbox,
Control System Toolbox,
Navigation Toolbox,
Simscape,
Simscape Multibody,
UAV Toolbox,
Robotics System Toolbox,
Robust Control Toolbox,
Symbolic Math Toolbox

## Library requirements til Python program til data behandling:
### Python 3.11,
pandas,
matplotlib,
numpy,
fastdtw,
scipy