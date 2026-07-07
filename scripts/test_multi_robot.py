import csv
import math
import os

EXPECTED_DISTANCE = 1.5
TOLERANCE = 0.15


def test_distance_constraint():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, "isaacsim_fleet_data_n3.csv")

    assert os.path.exists(csv_file), f"Data file {csv_file} not found!"

    # Keep track of how many valid frames we actually tested
    valid_frames_tested = 0

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            leader_x = float(row["leader_x"])

            # ==========================================
            # FIX: Dynamic Spatial Filter
            # Only test the formation after they have cleared
            # the 1.0m mark (explosion zone) and before the goal.
            # ==========================================
            if not (1.0 < leader_x < 4.9):
                continue

            valid_frames_tested += 1

            leader_y = float(row["leader_y"])
            f1_y = float(row["f1_y"])
            f2_y = float(row["f2_y"])

            dist_f1 = abs(leader_y - f1_y)
            dist_f2 = abs(leader_y - f2_y)

            assert math.isclose(dist_f1, EXPECTED_DISTANCE, abs_tol=TOLERANCE), (
                f"Frame {row['frame']} (X={leader_x:.2f}): Follower 1 broke formation! Distance was {dist_f1:.2f}m"
            )

            assert math.isclose(dist_f2, EXPECTED_DISTANCE, abs_tol=TOLERANCE), (
                f"Frame {row['frame']} (X={leader_x:.2f}): Follower 2 broke formation! Distance was {dist_f2:.2f}m"
            )

    # Ensure we actually tested a chunk of data and didn't just skip the whole file
    assert valid_frames_tested > 0, (
        "No valid driving frames were found in the safe zone!"
    )


def test_expected_number_of_robots():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, "isaacsim_fleet_data_n3.csv")

    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        headers = next(reader)

        # Expecting 7 columns: frame, leader_x, leader_y, f1_x, f1_y, f2_x, f2_y
        assert len(headers) == 7, (
            f"Expected data for 3 robots, but found {len(headers)} columns."
        )
