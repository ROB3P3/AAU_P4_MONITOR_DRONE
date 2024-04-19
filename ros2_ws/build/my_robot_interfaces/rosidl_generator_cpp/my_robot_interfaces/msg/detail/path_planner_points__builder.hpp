// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_robot_interfaces:msg/PathPlannerPoints.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__MSG__DETAIL__PATH_PLANNER_POINTS__BUILDER_HPP_
#define MY_ROBOT_INTERFACES__MSG__DETAIL__PATH_PLANNER_POINTS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_robot_interfaces/msg/detail/path_planner_points__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_PathPlannerPoints_col
{
public:
  explicit Init_PathPlannerPoints_col(::my_robot_interfaces::msg::PathPlannerPoints & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::msg::PathPlannerPoints col(::my_robot_interfaces::msg::PathPlannerPoints::_col_type arg)
  {
    msg_.col = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::msg::PathPlannerPoints msg_;
};

class Init_PathPlannerPoints_row
{
public:
  explicit Init_PathPlannerPoints_row(::my_robot_interfaces::msg::PathPlannerPoints & msg)
  : msg_(msg)
  {}
  Init_PathPlannerPoints_col row(::my_robot_interfaces::msg::PathPlannerPoints::_row_type arg)
  {
    msg_.row = std::move(arg);
    return Init_PathPlannerPoints_col(msg_);
  }

private:
  ::my_robot_interfaces::msg::PathPlannerPoints msg_;
};

class Init_PathPlannerPoints_data
{
public:
  Init_PathPlannerPoints_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PathPlannerPoints_row data(::my_robot_interfaces::msg::PathPlannerPoints::_data_type arg)
  {
    msg_.data = std::move(arg);
    return Init_PathPlannerPoints_row(msg_);
  }

private:
  ::my_robot_interfaces::msg::PathPlannerPoints msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::msg::PathPlannerPoints>()
{
  return my_robot_interfaces::msg::builder::Init_PathPlannerPoints_data();
}

}  // namespace my_robot_interfaces

#endif  // MY_ROBOT_INTERFACES__MSG__DETAIL__PATH_PLANNER_POINTS__BUILDER_HPP_
