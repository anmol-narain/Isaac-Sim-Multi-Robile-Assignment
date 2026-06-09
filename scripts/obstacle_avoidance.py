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


def forward(speed=5.0):

    pos = robot.get_joint_positions()[0].copy()

    for i in range(4):
        pos[i] = 0.0

    robot.set_joint_positions(pos)

    vel = [0.0] * robot.num_dof

    for i in range(4, 12):
        vel[i] = speed

    robot.set_joint_velocities(vel)


def turn_left(speed=5.0, steering_angle=0.7):

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


def get_front_distance():

    xform = UsdGeom.Xformable(laser_prim)

    world_transform = xform.ComputeLocalToWorldTransform(0)

    origin = world_transform.ExtractTranslation()

    direction = world_transform.TransformDir(Gf.Vec3d(1.0, 0.0, 0.0))

    direction.Normalize()

    origin = origin + direction * 0.20

    hit = physx_query.raycast_closest(origin, direction, 10.0)

    if hit["hit"]:
        return hit["distance"]

    return 10.0


# =====================================================
# Callback
# =====================================================


def on_update(event):

    distance = get_front_distance()

    print(f"Distance: {distance:.2f}")

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
