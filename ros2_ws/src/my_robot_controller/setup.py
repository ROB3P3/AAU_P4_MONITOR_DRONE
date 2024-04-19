from setuptools import find_packages, setup

package_name = 'my_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='drone',
    maintainer_email='drone@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_node = my_robot_controller.my_first_node:main",
            "test_node2 = my_robot_controller.my_seccond_node:main",
            "my_talker = my_robot_controller.my_talker:main",
            "my_listener = my_robot_controller.my_listener:main",
            "crazy_node = my_robot_controller.crazy_flie_radio_test:main",
            "crazy_node_take_off = my_robot_controller.crazy_flie_positioning:main",
            "vicon_node = my_robot_controller.vicon_node:main",
        ],
    },
)
