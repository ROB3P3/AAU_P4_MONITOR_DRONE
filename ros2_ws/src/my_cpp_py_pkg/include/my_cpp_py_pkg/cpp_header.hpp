#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include <iostream>
#include <fstream>
#include <chrono>
#include <string.h>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "Linux64/DataStreamRetimingClient.h"


class MyCustomNode : public rclcpp::Node
{
    public:
        MyCustomNode(): Node("my_node") {
            RCLCPP_INFO(this->get_logger(), "TEST Cpp node 2");
        }
    private:
};


class ViconClient : public rclcpp::Node
{   
    public:
        ViconClient(): Node("my_vicon_client") {
            ///Output_GetVersion Output = MyClient.GetVersion();
            RCLCPP_INFO(this->get_logger(), "Version");
            ViconDataStreamSDK::CPP::RetimingClient ViconRetimingClient;  ///Retimer.Connect("localhost:801");
            ViconDataStreamSDK::CPP::Output_GetVersion output = ViconRetimingClient.GetVersion();
            RCLCPP_INFO(this->get_logger(),"Version igem '%d'", output.Major);
            ViconRetimingClient.Connect("localhost", 30);

            while (ViconRetimingClient.IsConnected())
            {
                ViconDataStreamSDK::CPP::Output_WaitForFrame WaitOutput = ViconRetimingClient.WaitForFrame();
                if (WaitOutput.Result == ViconDataStreamSDK::CPP::Result::Success)
                {
                    ViconDataStreamSDK::CPP::Output_UpdateFrame frame = ViconRetimingClient.UpdateFrame();
                }
            }


        }
};

using namespace std::chrono_literals;

class MyPublisher : public rclcpp::Node
{
    public:
        MyPublisher()
        : Node("my_cpp_publisher"), count_(0)
        {
            publisher_ = this->create_publisher<std_msgs::msg::String>("we_are_talking", 10);
            timer_ = this->create_wall_timer(
                500ms, std::bind(&MyPublisher::timer_callback, this));
        }
    private:
        void timer_callback()
        {
            auto message = std_msgs::msg::String();
            message.data = "Hellow World" + std::to_string(count_++);
            RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
            publisher_->publish(message);
        }
        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
        size_t count_;
};

