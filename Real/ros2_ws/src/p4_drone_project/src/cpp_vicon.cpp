#include "rclcpp/rclcpp.hpp"
#include "p4_drone_project/cpp_header.hpp"

int main(int argc, char **argv)
{
	rclcpp::init(argc, argv);
	auto node = std::make_shared<ViconClient>();
	rclcpp::spin(node);
	rclcpp::shutdown();

	return 0;
}