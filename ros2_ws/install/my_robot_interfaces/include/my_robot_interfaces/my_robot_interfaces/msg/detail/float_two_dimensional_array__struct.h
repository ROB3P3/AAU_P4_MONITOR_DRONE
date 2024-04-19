// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_robot_interfaces:msg/FloatTwoDimensionalArray.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__MSG__DETAIL__FLOAT_TWO_DIMENSIONAL_ARRAY__STRUCT_H_
#define MY_ROBOT_INTERFACES__MSG__DETAIL__FLOAT_TWO_DIMENSIONAL_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'data'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/FloatTwoDimensionalArray in the package my_robot_interfaces.
typedef struct my_robot_interfaces__msg__FloatTwoDimensionalArray
{
  rosidl_runtime_c__double__Sequence data;
} my_robot_interfaces__msg__FloatTwoDimensionalArray;

// Struct for a sequence of my_robot_interfaces__msg__FloatTwoDimensionalArray.
typedef struct my_robot_interfaces__msg__FloatTwoDimensionalArray__Sequence
{
  my_robot_interfaces__msg__FloatTwoDimensionalArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_robot_interfaces__msg__FloatTwoDimensionalArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_ROBOT_INTERFACES__MSG__DETAIL__FLOAT_TWO_DIMENSIONAL_ARRAY__STRUCT_H_
