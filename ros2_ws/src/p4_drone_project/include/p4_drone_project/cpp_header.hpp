#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include <iostream>
#include <fstream>
#include <chrono>
#include <string.h>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"
#include "Linux64/DataStreamRetimingClient.h"

using namespace std::chrono_literals;

class ViconClient : public rclcpp::Node
{   
    public:
        ViconClient(): Node("my_vicon_client") 
        {
            viconPubliser_ = this->create_publisher<std_msgs::msg::Float64MultiArray>("pid_regulator_vicon", 10);
            ///Output_GetVersion Output = MyClient.GetVersion();
            RCLCPP_INFO(this->get_logger(), "Version");
            ViconDataStreamSDK::CPP::RetimingClient ViconRetimingClient; 
            ViconDataStreamSDK::CPP::Output_GetVersion output = ViconRetimingClient.GetVersion();
            RCLCPP_INFO(this->get_logger(),"Version igem '%d'", output.Major);
            
            ViconRetimingClient.Connect("192.168.1.33:801", 10.0);

            ViconDataStreamSDK::CPP::Output_IsConnected clientIsConnected = ViconRetimingClient.IsConnected();

            RCLCPP_INFO(this->get_logger(), "Attempting to connect to vicon!");
            while (clientIsConnected.Connected)
            {
                RCLCPP_INFO(this->get_logger(), "Connected to Vicon");
                // if connection get info about drone and publish it to the "pid_regulator_vicon" topic
                ViconDataStreamSDK::CPP::Output_UpdateFrame frame = ViconRetimingClient.UpdateFrame();
                ViconDataStreamSDK::CPP::Output_GetSubjectCount viconSubjectCount = ViconRetimingClient.GetSubjectCount();
                if(viconSubjectCount.Result == ViconDataStreamSDK::CPP::Result::Success)
                {
                    for (unsigned int SubjectIndex = 0; SubjectIndex < viconSubjectCount.SubjectCount; ++SubjectIndex)
                    {
                        ViconDataStreamSDK::CPP::Output_GetSubjectName subjectName = ViconRetimingClient.GetSubjectName(SubjectIndex);
                        if(subjectName.Result == ViconDataStreamSDK::CPP::Result::Success)
                        {
                            ViconDataStreamSDK::CPP::Output_GetSegmentCount segmentCount = ViconRetimingClient.GetSegmentCount(subjectName.SubjectName);
                            if(segmentCount.Result == ViconDataStreamSDK::CPP::Result::Success)
                            {
                                for (unsigned int SegmentIndex = 0; SegmentIndex < segmentCount.SegmentCount; ++SegmentIndex)
                                {
                                    ViconDataStreamSDK::CPP::Output_GetSegmentName segmentName = ViconRetimingClient.GetSegmentName(subjectName.SubjectName, SegmentIndex);
                                    if(segmentName.Result == ViconDataStreamSDK::CPP::Result::Success)
                                    {
                                        ViconDataStreamSDK::CPP::Output_GetSegmentGlobalTranslation globalTranslation = ViconRetimingClient.GetSegmentGlobalTranslation(subjectName.SubjectName, segmentName.SegmentName);
                                        ViconDataStreamSDK::CPP::Output_GetSegmentLocalRotationEulerXYZ globalRotation = ViconRetimingClient.GetSegmentLocalRotationEulerXYZ(subjectName.SubjectName, segmentName.SegmentName);
                                        if(globalTranslation.Result == ViconDataStreamSDK::CPP::Result::Success && globalRotation.Result == ViconDataStreamSDK::CPP::Result::Success)
                                        {
                                            auto message = std_msgs::msg::Float64MultiArray();
                                            message.data = {globalTranslation.Translation[0], globalTranslation.Translation[1], globalTranslation.Translation[2], globalRotation.Rotation[2]};
                                            RCLCPP_INFO(this->get_logger(), "Publishing: '[%f, %f, %f]'", message.data[0], message.data[1], message.data[2], message.data[3]);
                                            viconPubliser_->publish(message);
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            //timer_ = this->create_wall_timer(333ms, std::bind(&ViconClient::timer_callback, this));
        }
    private:
        void timer_callback()
        {
            auto message = std_msgs::msg::Float64MultiArray();
            message.data = {0.0, 1.0, 2.0, 3.0};
            RCLCPP_INFO(this->get_logger(), "Publishing: '[%f, %f, %f, %f]'", message.data[0], message.data[1], message.data[2], message.data[3]);
            viconPubliser_->publish(message);
        }
        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr viconPubliser_;
};