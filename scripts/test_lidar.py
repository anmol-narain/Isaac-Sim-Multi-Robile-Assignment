import omni.usd
from pxr import Usd

stage = omni.usd.get_context().get_stage()

lidar = stage.GetPrimAtPath(
    "/robile3_config/base_link/base_laser_mount/base_laser/lidar"
)

print("Prim Type:", lidar.GetTypeName())

for attr in lidar.GetAttributes():
    print(attr.GetName())
