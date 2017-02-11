#!/usr/bin/env python
import rospy
from hw_api_ackermann.msg import AckermannDrive
from std_msgs.msg import Bool

class TruckMaster:
    def __init__(self):
        self.dead_mans_switch = False
        self.auto_ctrl = False
        self.pub = rospy.Publisher('master_drive', AckermannDrive, queue_size=10)

        rospy.init_node('master', anonymous=False)
        rospy.Subscriber('auto_drive', AckermannDrive, self.autAckermannHandler)
        rospy.Subscriber('man_drive', AckermannDrive, self.manualAckermannHandler)
        rospy.Subscriber('auto_ctrl', Bool, self.manualOrAutomaticHandler)
        rospy.Subscriber('dead_mans_switch', Bool, self.goHandler)

    def autoDriveHandler(self,data):
        if self.auto_ctrl and self.dead_mans_switch:
            self.pub.publish(data)

    def manualDriveHandler(self,data):
        if (not self.auto_ctrl) and self.dead_mans_switch:
            self.pub.publish(data)

    def autoCtrlHandler(self,data):
        self.auto_ctrl = data.data

    def deadMansSwitchHandler(self,data):
        self.dead_mans_switch = data.data
        if not self.dead_mans_switch:
            ack = AckermannDrive()
            ack.steering_angle = 0
            ack.speed = 0
            self.pub.publish(ack)

if __name__ == '__main__':
    tm = TruckMaster()
    rospy.spin()
