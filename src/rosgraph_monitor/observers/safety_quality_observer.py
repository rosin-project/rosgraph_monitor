from rosgraph_monitor.observer import TopicObserver
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from diagnostic_msgs.msg import DiagnosticStatus, KeyValue
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from math import sqrt


class SafetyQualityObserver(TopicObserver):
    def __init__(self, name):
        topics = [("/odom", Odometry), ("/imu/data", Imu), ("/d_obstacle", Float32)]     # list of pairs

        super(SafetyQualityObserver, self).__init__(
            name, 10, topics)


    def calculate_attr(self, msgs):
        status_msg = DiagnosticStatus()

        vel_x = msgs[0].twist.twist.linear.x
        vel_y = msgs[0].twist.twist.linear.y

        velocity = sqrt(vel_x ** 2 + vel_y ** 2)


        ## We assume a max acceleration of 1 m/s^2
        ## The minimum value
        d_break = (velocity)/(0.4)

       # print (d_break)
        normalized_safety=1.0
        if (d_break > msgs[2].data):
            normalized_safety = msgs[2].data/d_break

        #print ("d_break: {0}".format(d_break))
        #print("disntace:{0}".format(msgs[2].data))
        print("normalized safety:{0}".format(normalized_safety))
        status_msg = DiagnosticStatus()
        status_msg.level = DiagnosticStatus.OK
        status_msg.name = self._id
        status_msg.values.append(
            KeyValue("safety", str(normalized_safety)))
        status_msg.message = "QA status"

        return status_msg
