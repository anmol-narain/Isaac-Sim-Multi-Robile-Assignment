import omni.kit.commands

# Create RTX LiDAR under the existing laser frame

omni.kit.commands.execute(
    "IsaacSensorCreateRtxLidar",
    path="/robile3_config/base_link/base_laser_mount/base_laser/lidar",
    config="Example_Rotary",
)

print("LiDAR created")
