// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_robot_interfaces:srv/StopPublishPath.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__SRV__DETAIL__STOP_PUBLISH_PATH__BUILDER_HPP_
#define MY_ROBOT_INTERFACES__SRV__DETAIL__STOP_PUBLISH_PATH__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_robot_interfaces/srv/detail/stop_publish_path__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_robot_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::srv::StopPublishPath_Request>()
{
  return ::my_robot_interfaces::srv::StopPublishPath_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_StopPublishPath_Response_success
{
public:
  Init_StopPublishPath_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::my_robot_interfaces::srv::StopPublishPath_Response success(::my_robot_interfaces::srv::StopPublishPath_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::srv::StopPublishPath_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::srv::StopPublishPath_Response>()
{
  return my_robot_interfaces::srv::builder::Init_StopPublishPath_Response_success();
}

}  // namespace my_robot_interfaces

#endif  // MY_ROBOT_INTERFACES__SRV__DETAIL__STOP_PUBLISH_PATH__BUILDER_HPP_
