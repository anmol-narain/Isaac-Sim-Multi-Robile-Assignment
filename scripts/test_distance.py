import omni.physx
import omni.usd
from pxr import Gf, UsdGeom

stage = omni.usd.get_context().get_stage()

laser_path = "/robile3_config/base_link/base_laser_mount/base_laser"

laser_prim = stage.GetPrimAtPath(laser_path)

xform = UsdGeom.Xformable(laser_prim)
world_transform = xform.ComputeLocalToWorldTransform(0)

origin = world_transform.ExtractTranslation()

# Forward direction of the laser
direction = world_transform.TransformDir(Gf.Vec3d(1.0, 0.0, 0.0))

direction.Normalize()

physx_query = omni.physx.get_physx_scene_query_interface()

hit = physx_query.raycast_closest(origin, direction, 10.0)

print("Origin:", origin)
print("Direction:", direction)
print("Hit:", hit)
