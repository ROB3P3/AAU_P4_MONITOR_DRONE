// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_robot_interfaces:msg/FloatTwoDimensionalArray.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__MSG__DETAIL__FLOAT_TWO_DIMENSIONAL_ARRAY__BUILDER_HPP_
#define MY_ROBOT_INTERFACES__MSG__DETAIL__FLOAT_TWO_DIMENSIONAL_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_robot_interfaces/msg/detail/float_two_dimensional_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_FloatTwoDimensionalArray_data
{
public:
  Init_FloatTwoDimensionalArray_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::my_robot_interfaces::msg::FloatTwoDimensionalArray data(::my_robot_interfaces::msg::FloatTwoDimensionalArray::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::msg::FloatTwoDimensionalArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::msg::FloatTwoDimensionalArray>()
{
  return my_robot_interfaces::msg::builder::Init_FloatTwoDimensionalArray_data();
}

}  // namespace my_robot_interfaces

#endif  // MY_ROBOT_INTERFACES__MSG__DETAIL__FLOAT_TWO_DIMENSIONAL_ARRAY__BUILDER_HPP_
