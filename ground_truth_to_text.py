
#Ground Truth#
# FOR ORB use (afteer source) rosservice call /orb_slam3/save_traj abbc.txt after entire data is run
#DATA

import rospy
from geometry_msgs.msg import PoseStamped

f = open("outputx.txt", "w")
g = open("outputy.txt", "w")
h = open("outputz.txt", "w")

def callback(data):
    x = data.pose.position.x
    y = data.pose.position.y
    z = data.pose.position.z

    f.write(float(x))
    g.write(float(y))
    h.write(float(z))

def listener():

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/vicon_client/METRICS/pose", PoseStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()


