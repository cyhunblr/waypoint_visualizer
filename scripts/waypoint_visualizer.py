#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import csv
import rospy,rospkg
from visualization_msgs.msg import MarkerArray, Marker
from std_msgs.msg import Empty

"""
Csv file must be include respectively "x,y,z,yaw,velocity,change_flag"
"""

class Visualizer():

    def __init__(self):

        self.wp_publisher = rospy.Publisher("/waypoints_publisher", MarkerArray, queue_size=100)

        self.package_name = rospy.get_param('~package_name',"waypoint_visualizer")
        self.file_name = rospy.get_param('~file_name',"waypoints.csv")
        self.frame_id = rospy.get_param('~frame_id',"map")
        self.scale_x = rospy.get_param('~scale_x',"0.3")
        self.scale_y = rospy.get_param('~scale_y',"0.3")
        self.scale_z = rospy.get_param('~scale_z',"0.3")
        self.color_r = rospy.get_param('~color_r',"1.0")
        self.color_g = rospy.get_param('~color_g',"0.0")
        self.color_b = rospy.get_param('~color_b',"0.0")
        
        while not rospy.is_shutdown():
                
                rows = self.reader()
                markerArray = MarkerArray()

                rospy.loginfo("Publishing waypoints!")
                rospy.sleep(2.)
                
                for wp in rows:
                        marker = Marker()
                        marker.header.frame_id = self.frame_id
                        marker.type = marker.SPHERE
                        marker.action = marker.ADD
                        marker.scale.x = self.scale_x
                        marker.scale.y = self.scale_y
                        marker.scale.z = self.scale_z
                        marker.color.a = 1.0
                        marker.color.r = self.color_r
                        marker.color.g = self.color_g
                        marker.color.b = self.color_b
                        marker.pose.orientation.w = 1.0
                        marker.lifetime = rospy.Duration()
                        marker.pose.position.x = float(wp[0])
                        marker.pose.position.y = float(wp[1])
                        marker.pose.position.z = float(wp[2])
                        marker.id = self.count

                        markerArray.markers.append(marker)
                        self.count +=1

                        self.wp_publisher.publish(markerArray)


                break

    def reader(self):

        self.count = 0
        num_rows = 0
        rows = []
        r = rospkg.RosPack()
        package_path = r.get_path(self.package_name)
        file_path = package_path + "/waypoints/" + self.file_name
        rospy.loginfo("Reading CSV file!")
        with open(file_path) as f:
                csvreader = csv.reader(f)
                header = next(csvreader)
                for row in csvreader:
                        num_rows += 1
                        rows.append(row[0:6])
        return rows


if __name__ == "__main__":

    try:
        rospy.init_node('waypoints_publisher')
        wp = Visualizer()
        rospy.spin()
    except Exception as error:
        rospy.loginfo("An exception occurred: {}".format(error))