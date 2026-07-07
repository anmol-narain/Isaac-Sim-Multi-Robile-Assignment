import csv
import os

import omni.kit.app
import omni.usd
from isaacsim.core.prims import Articulation

leader = Articulation("/robile_leader/base_link")
follower_1 = Articulation("/robile_follower_1/base_link")

leader.initialize()
follower_1.initialize()

fleet = [leader, follower_1]

GOAL_X = 5.0
TOLERANCE = 0.1

csv_path = os.path.expanduser(
    "~/isaac_projects/robile_assignment/scripts/isaacsim_fleet_data_n2.csv"
)
# Only 5 columns needed
csv_data = [["frame", "leader_x", "leader_y", "f1_x", "f1_y"]]

WARM_UP_FRAMES = 300
total_frames_elapsed = 0
logging_frame_counter = 0
mission_complete = False


def move_fleet(speed):
    for robot in fleet:
        pos = robot.get_joint_positions()[0].copy()
        for i in range(4):
            pos[i] = 0.0
        robot.set_joint_positions(pos)
        vel = [0.0] * robot.num_dof
        for i in range(4, 12):
            vel[i] = speed
        robot.set_joint_velocities(vel)


def stop_fleet():
    move_fleet(0.0)


def on_update(event):
    global total_frames_elapsed, logging_frame_counter, mission_complete

    if mission_complete:
        return

    total_frames_elapsed += 1
    if total_frames_elapsed < WARM_UP_FRAMES:
        print(
            f"Warming up physics... {total_frames_elapsed}/{WARM_UP_FRAMES}    ",
            end="\r",
        )
        return

    l_pos, _ = leader.get_world_poses()
    f1_pos, _ = follower_1.get_world_poses()

    current_x = l_pos[0][0]

    csv_data.append(
        [logging_frame_counter, l_pos[0][0], l_pos[0][1], f1_pos[0][0], f1_pos[0][1]]
    )
    logging_frame_counter += 1

    print(f"Leader X: {current_x:.2f} / {GOAL_X:.2f}    ", end="\r")

    if current_x < (GOAL_X - TOLERANCE):
        move_fleet(speed=-5.0)
    else:
        stop_fleet()
        mission_complete = True
        with open(csv_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)
        print(f"\nGoal Reached! Clean data saved to: {csv_path}")


stream = omni.kit.app.get_app().get_update_event_stream()
subscription = stream.create_subscription_to_pop(on_update, name="FleetNavigation_N2")
