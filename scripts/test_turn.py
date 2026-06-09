from isaacsim.core.prims import Articulation

robot = Articulation("/robile3_config/base_link")
robot.initialize()

vel = [0.0] * robot.num_dof

# Left wheels
vel[4] = -5
vel[6] = -5
vel[8] = -5
vel[10] = -5

# Right wheels
vel[5] = 5
vel[7] = 5
vel[9] = 5
vel[11] = 5

robot.set_joint_velocities(vel)

print("Turn test")
