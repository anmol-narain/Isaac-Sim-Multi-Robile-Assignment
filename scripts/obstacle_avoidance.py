import omni.kit.app
import omni.physx
import omni.usd
from isaacsim.core.prims import Articulation
from pxr import Gf, UsdGeom

# =====================================================
# Robot
# =====================================================

robot = Articulation("/robile3_config/base_link")
robot.initialize()

# =====================================================
# Sensor
# =====================================================

stage = omni.usd.get_context().get_stage()

laser_prim = stage.GetPrimAtPath(
    "/robile3_config/base_link/base_laser_mount/base_laser"
)

physx_query = omni.physx.get_physx_scene_query_interface()

THRESHOLD = 1.0

# =====================================================
# Motion
# =====================================================


# BUG FIX 1: Changed default speed to -5.0 to align wheel rotation with LiDAR forward axis
def forward(speed=-5.0):

    # Note: [0] is correct if Isaac Sim is returning a 2D array for batched environments
    pos = robot.get_joint_positions()[0].copy()

    for i in range(4):
        pos[i] = 0.0

    robot.set_joint_positions(pos)

    vel = [0.0] * robot.num_dof

    for i in range(4, 12):
        vel[i] = speed

    robot.set_joint_velocities(vel)


# BUG FIX 2: Changed steering_angle to 1.57 (90 degrees) to strafe sideways
# Changed speed to match the inverted coordinate frame
def turn_left(speed=-5.0, steering_angle=1.57):

    pos = robot.get_joint_positions()[0].copy()

    for i in range(4):
        pos[i] = steering_angle

    robot.set_joint_positions(pos)

    vel = [0.0] * robot.num_dof

    for i in range(4, 12):
        vel[i] = speed

    robot.set_joint_velocities(vel)


# =====================================================
# Sensor Query
# =====================================================


# =====================================================
# Sensor Query (Upgraded to Multi-Ray LiDAR Sweep)
# =====================================================


def get_front_distance():
    xform = UsdGeom.Xformable(laser_prim)
    world_transform = xform.ComputeLocalToWorldTransform(0)
    origin = world_transform.ExtractTranslation()

    # Define a spread of rays to simulate a LiDAR sweep
    # (Center, Slight Left, Slight Right, Wide Left, Wide Right)
    ray_directions = [
        Gf.Vec3d(1.0, 0.0, 0.0),
        Gf.Vec3d(1.0, 0.4, 0.0),
        Gf.Vec3d(1.0, -0.4, 0.0),
        Gf.Vec3d(1.0, 0.8, 0.0),
        Gf.Vec3d(1.0, -0.8, 0.0),
    ]

    min_distance = 10.0

    for local_dir in ray_directions:
        direction = world_transform.TransformDir(local_dir)
        direction.Normalize()

        # Offset origin slightly forward to avoid hitting the robot's own chassis
        start_point = origin + direction * 0.20

        hit = physx_query.raycast_closest(start_point, direction, 10.0)

        # If any ray hits something closer than our current minimum, update it
        if hit["hit"] and hit["distance"] < min_distance:
            min_distance = hit["distance"]

    # Returns the distance of the CLOSEST object in the entire forward cone
    return min_distance


# =====================================================
# Callback
# =====================================================


def on_update(event):

    distance = get_front_distance()

    # Print with carriage return formatting to keep console clean
    print(f"Distance: {distance:.2f}    ", end="\r")

    if distance < THRESHOLD:
        turn_left()
    else:
        forward()


# =====================================================
# Register
# =====================================================

stream = omni.kit.app.get_app().get_update_event_stream()

subscription = stream.create_subscription_to_pop(on_update, name="ObstacleAvoidance")

print("Obstacle avoidance running")
