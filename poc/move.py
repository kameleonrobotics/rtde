import math
import math3d as m3d
import time

import URBasic

ROBOT_IP = '192.168.247.128'
ACCELERATION = 0.9  # Robot acceleration value
VELOCITY = 0.8  # Robot speed value
freq = 125  # Hz

# The Joint position the robot starts at
robot_start_position = (math.radians(-218),
                        math.radians(-63),
                        math.radians(-93),
                        math.radians(-20),
                        math.radians(88),
                        math.radians(0))

print("initialising robot")
robotModel = URBasic.robotModel.RobotModel()
robot = URBasic.urScriptExt.UrScriptExt(host=ROBOT_IP, robotModel=robotModel)

robot.reset_error()
print("robot initialised")
time.sleep(1)

# Move Robot to the midpoint of the lookplane
robot.movej(q=robot_start_position, a=ACCELERATION, v=VELOCITY)

robot.init_realtime_control()  # starts the realtime control loop on the Universal-Robot Controller
time.sleep(1)  # just a short wait to make sure everything is initialised

try:
    # while True:
        # robot.set_realtime_pose(next_pose)
    time.sleep(1/freq)
    tcp_pos = robot.get_actual_tcp_pose()
    print(f"{tcp_pos=}")

    robot.movej([-1.16756324, 0.3570666, 1.08672699, -1.39822642, -0.64988366, 0.70045013])
    robot.movej([-1.16756324, 1.3570666, 1.08672699, -1.39822642, -0.64988366, 0.70045013])

except KeyboardInterrupt:
    print("closing robot connection")
    robot.close()
