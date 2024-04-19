// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_robot_interfaces:srv/StopPublishPath.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__SRV__DETAIL__STOP_PUBLISH_PATH__STRUCT_H_
#define MY_ROBOT_INTERFACES__SRV__DETAIL__STOP_PUBLISH_PATH__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/StopPublishPath in the package my_robot_interfaces.
typedef struct my_robot_interfaces__srv__StopPublishPath_Request
{
  uint8_t structure_needs_at_least_one_member;
} my_robot_interfaces__srv__StopPublishPath_Request;

// Struct for a sequence of my_robot_interfaces__srv__StopPublishPath_Request.
typedef struct my_robot_interfaces__srv__StopPublishPath_Request__Sequence
{
  my_robot_interfaces__srv__StopPublishPath_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_robot_interfaces__srv__StopPublishPath_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/StopPublishPath in the package my_robot_interfaces.
typedef struct my_robot_interfaces__srv__StopPublishPath_Response
{
  bool success;
} my_robot_interfaces__srv__StopPublishPath_Response;

// Struct for a sequence of my_robot_interfaces__srv__StopPublishPath_Response.
typedef struct my_robot_interfaces__srv__StopPublishPath_Response__Sequence
{
  my_robot_interfaces__srv__StopPublishPath_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_robot_interfaces__srv__StopPublishPath_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_ROBOT_INTERFACES__SRV__DETAIL__STOP_PUBLISH_PATH__STRUCT_H_
