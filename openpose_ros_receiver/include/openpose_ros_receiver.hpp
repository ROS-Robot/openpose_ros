#ifndef _OPENPOSE_ROS_RECEIVER_H_
#define _OPENPOSE_ROS_RECEIVER_H_

/* OpenPose ROS wrapper headers */
#include <openpose_ros_msgs/BoundingBox.h>
#include <openpose_ros_msgs/OpenPoseHuman.h>
#include <openpose_ros_msgs/OpenPoseHumanList.h>
#include <openpose_ros_msgs/PointWithProb.h>
#include <openpose_ros_receiver_msgs/OpenPoseReceiverHuman.h>
#include <openpose_ros_receiver_msgs/OpenPoseReceiverKeypoint.h>

/* ROS headers */
#include <ros/ros.h>
#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/approximate_time.h>
#include <std_msgs/String.h>

/* TF headers */
#include <tf/transform_broadcaster.h>
#include <tf/transform_listener.h>

/* PCL headers */
#include <sensor_msgs/PointCloud2.h>
#include <pcl_ros/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/common/common.h>

/* C++ headers */
#include <fstream>
#include <ctime>
#include <sstream>
#include <cmath>

/* C headers */
#include <assert.h>   // for development phase

/* OpenPose headers */
#include <openpose/pose/poseParameters.hpp>

/* Important definitions */
#define RELIABILITY_THRESHOLD 3.0           // seconds -> float
#define MAX_RETRY 2                         // number of repetitions -> int
#define TF_WAIT 10                          // seconds -> float
#define IMG_PIXEL_WIDTH 672                 // pixels
#define IMG_PIXEL_HEIGHT 376                // pixels
#define UPPER_VARIATION_THRESH 1.15         // how much different is the avg neighborhood value allowed to be in contrast to the point value --> float
#define LOWER_VARIATION_THRESH 0.85         // how much different is the avg neighborhood value allowed to be in contrast to the point value --> float

/* Global Variables */
extern bool tfSubtree, logging, pclMsg, humanListMsg;
extern std::string image_sensor_frame;
extern ros::Publisher robotFrameCoordsPub, humanReceiverPub, pointcloudDebugPub;
extern pcl::PointCloud<pcl::PointXYZRGBA>::Ptr pPCL;

/* OpenPose BODY_25 Body Parts Index-to-Name Mapping */
const std::map<unsigned int, std::string> POSE_BODY_25_BODY_PARTS
{
    {0,  "Nose"},
    {1,  "Neck"},
    {2,  "RShoulder"},
    {3,  "RElbow"},
    {4,  "RWrist"},
    {5,  "LShoulder"},
    {6,  "LElbow"},
    {7,  "LWrist"},
    {8,  "MidHip"},
    {9,  "RHip"},
    {10, "RKnee"},
    {11, "RAnkle"},
    {12, "LHip"},
    {13, "LKnee"},
    {14, "LAnkle"},
    {15, "REye"},
    {16, "LEye"},
    {17, "REar"},
    {18, "LEar"},
    {19, "LBigToe"},
    {20, "LSmallToe"},
    {21, "LHeel"},
    {22, "RBigToe"},
    {23, "RSmallToe"},
    {24, "RHeel"},
    {25, "Background"}
};

/* Broadcaster's and Receiver's Node functions */

/* Callback functions */
void pointCloudTopicCallback(const pcl::PointCloud<pcl::PointXYZRGBA>::Ptr& pPCL);
void humanListCallback(const openpose_ros_msgs::OpenPoseHumanList::ConstPtr& list_msg);

/* Various functions */
void listenForSkeleton(const openpose_ros_msgs::OpenPoseHumanList::ConstPtr& msg);
std::string getPoseBodyPartMappingBody25(unsigned int idx);

#endif