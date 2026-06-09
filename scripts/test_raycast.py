import omni.physx
import omni.usd
from pxr import UsdGeom

stage = omni.usd.get_context().get_stage()

laser_path = "/robile3_config/base_link/base_laser_mount/base_laser"

laser_prim = stage.GetPrimAtPath(laser_path)

xform = UsdGeom.Xformable(laser_prim)

world_transform = xform.ComputeLocalToWorldTransform(0)

origin = world_transform.ExtractTranslation()

print("Laser origin:", origin)

physx_query = omni.physx.get_physx_scene_query_interface()

print("Scene Query:", physx_query)
