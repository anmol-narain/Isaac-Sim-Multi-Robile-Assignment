from isaacsim.core.prims import Articulation

ROBOT_PATH = "/robile3_config/base_link"

robot = Articulation(ROBOT_PATH)
robot.initialize()


def stop():
    """Stop all wheel motion."""
    vel = [0.0] * robot.num_dof
    robot.set_joint_velocities(vel)


def forward(speed=5.0):
    """
    Drive straight.
    Steering = 0
    """

    pos = robot.get_joint_positions()[0].copy()

    for i in range(4):
        pos[i] = 0.0

    robot.set_joint_positions(pos)

    vel = [0.0] * robot.num_dof

    for i in range(4, 12):
        vel[i] = speed

    robot.set_joint_velocities(vel)


def turn_left(speed=5.0, steering_angle=0.7):
    """
    Drive diagonally left.
    """

    pos = robot.get_joint_positions()[0].copy()

    for i in range(4):
        pos[i] = steering_angle

    robot.set_joint_positions(pos)

    vel = [0.0] * robot.num_dof

    for i in range(4, 12):
        vel[i] = speed

    robot.set_joint_velocities(vel)


def turn_right(speed=5.0, steering_angle=-0.7):
    """
    Drive diagonally right.
    """

    pos = robot.get_joint_positions()[0].copy()

    for i in range(4):
        pos[i] = steering_angle

    robot.set_joint_positions(pos)

    vel = [0.0] * robot.num_dof

    for i in range(4, 12):
        vel[i] = speed

    robot.set_joint_velocities(vel)
