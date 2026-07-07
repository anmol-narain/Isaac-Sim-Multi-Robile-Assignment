import csv
import math
import os

EXPECTED_DISTANCE = 1.5
TOLERANCE = 0.15


# jdwdw
def test_distance_constraint_n2():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, "isaacsim_fleet_data_n2.csv")

    assert os.path.exists(csv_file), f"Data file {csv_file} not found!"

    valid_frames_tested = 0

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            leader_x = float(row["leader_x"])
            if not (2.5 < leader_x < 4.8):
                continue

            valid_frames_tested += 1
            leader_y = float(row["leader_y"])
            f1_y = float(row["f1_y"])

            dist_f1 = abs(leader_y - f1_y)
            assert math.isclose(dist_f1, EXPECTED_DISTANCE, abs_tol=TOLERANCE), (
                f"Frame {row['frame']} (X={leader_x:.2f}): Follower 1 broke formation! Distance was {dist_f1:.2f}m"
            )

    assert valid_frames_tested > 0, (
        "No valid driving frames were found in the safe zone!"
    )


def test_expected_number_of_robots_n2():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, "isaacsim_fleet_data_n2.csv")

    with open(csv_file, mode="r") as file:
        headers = next(csv.reader(file))
        assert len(headers) == 5, (
            f"Expected data for 2 robots, but found {len(headers)} columns."
        )
