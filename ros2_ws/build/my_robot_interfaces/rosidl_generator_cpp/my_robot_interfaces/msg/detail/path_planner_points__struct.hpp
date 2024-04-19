// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from my_robot_interfaces:msg/PathPlannerPoints.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__MSG__DETAIL__PATH_PLANNER_POINTS__STRUCT_HPP_
#define MY_ROBOT_INTERFACES__MSG__DETAIL__PATH_PLANNER_POINTS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__my_robot_interfaces__msg__PathPlannerPoints __attribute__((deprecated))
#else
# define DEPRECATED__my_robot_interfaces__msg__PathPlannerPoints __declspec(deprecated)
#endif

namespace my_robot_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PathPlannerPoints_
{
  using Type = PathPlannerPoints_<ContainerAllocator>;

  explicit PathPlannerPoints_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->row = 0ll;
      this->col = 0ll;
    }
  }

  explicit PathPlannerPoints_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->row = 0ll;
      this->col = 0ll;
    }
  }

  // field types and members
  using _data_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _data_type data;
  using _row_type =
    int64_t;
  _row_type row;
  using _col_type =
    int64_t;
  _col_type col;

  // setters for named parameter idiom
  Type & set__data(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->data = _arg;
    return *this;
  }
  Type & set__row(
    const int64_t & _arg)
  {
    this->row = _arg;
    return *this;
  }
  Type & set__col(
    const int64_t & _arg)
  {
    this->col = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_robot_interfaces__msg__PathPlannerPoints
    std::shared_ptr<my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_robot_interfaces__msg__PathPlannerPoints
    std::shared_ptr<my_robot_interfaces::msg::PathPlannerPoints_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PathPlannerPoints_ & other) const
  {
    if (this->data != other.data) {
      return false;
    }
    if (this->row != other.row) {
      return false;
    }
    if (this->col != other.col) {
      return false;
    }
    return true;
  }
  bool operator!=(const PathPlannerPoints_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PathPlannerPoints_

// alias to use template instance with default allocator
using PathPlannerPoints =
  my_robot_interfaces::msg::PathPlannerPoints_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace my_robot_interfaces

#endif  // MY_ROBOT_INTERFACES__MSG__DETAIL__PATH_PLANNER_POINTS__STRUCT_HPP_
