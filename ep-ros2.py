import rclpy
from rclpy.node import Node

import numpy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn

TOL = 0.001
DISTANCIA = 2
PI = 3.141592
X0 = 2.0
Y0 = 2.0

class TurtleFollower(Node):

    def __init__(self):
        super().__init__('turtle_follower')
        self._pose_subscriber = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        self._pose_subscriber_turtle2 = self.create_subscription(Pose, '/turtle2/pose', self.pose_callback_2, 10)
        self._vel_publisher_turtle2 = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)

        self._turtle_pose = Pose()
        self._turtle_pose_turtle2 = Pose()


    def pose_callback(self, msg):
        self._turtle_pose = msg
        msg = Twist()

        deltax = self._turtle_pose.x - self._turtle_pose_turtle2.x
        deltay = self._turtle_pose.y - self._turtle_pose_turtle2.y

        ang_0 = numpy.arctan(deltay/deltax)

        if deltax < 0 and deltay > 0:
            ang_0 += 3.141592

        elif deltax < 0 and deltay < 0:
            ang_0 -= 3.141592
        
        ang = self._turtle_pose_turtle2.theta - ang_0
        msg.angular.z = -ang*2
        dist = ( (self._turtle_pose_turtle2.y - self._turtle_pose.y)**2 + (self._turtle_pose_turtle2.x - self._turtle_pose.x)**2 )**(1/2)
        msg.linear.x = (dist - DISTANCIA)/DISTANCIA
        
        print(f"distância relativa: {dist} / ângulo relativo: {ang}")

        if abs(ang) < TOL:
            msg.angular.z = 0.0
            
        if abs(dist - DISTANCIA) < TOL:
            msg.linear.x = 0.0

        self._vel_publisher_turtle2.publish(msg)


    def pose_callback_2(self, msg):
        self._turtle_pose_turtle2 = msg


class PointPublisher(Node):

    def __init__(self):
        super().__init__('turtle_spawner')

        self.spawner = self.create_client(Spawn, 'spawn')
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        if self.spawner.service_is_ready():
            request = Spawn.Request()
            request.name = 'turtle2'
            request.x = float(X0)
            request.y = float(Y0)
            request.theta = float(0)
            self.result = self.spawner.call_async(request)
        else:
            self.get_logger().info('Service is not ready')



def main(args=None):
    rclpy.init(args=args)

    node = PointPublisher()
    rclpy.spin_once(node)

    turtle1 = TurtleFollower()
    rclpy.spin(turtle1)


if __name__ == '__main__':
    main()