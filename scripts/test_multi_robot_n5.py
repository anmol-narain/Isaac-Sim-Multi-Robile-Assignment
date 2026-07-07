import csv
import math
import os

# We assume followers 1 & 2 are 1.5m away, and followers 3 & 4 are 3.0m away
EXPECTED_DIST_INNER = 1.5
EXPECTED_DIST_OUTER = 3.0
TOLERANCE = 0.15


def test_distance_constraint_n5():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, "isaacsim_fleet_data_n5.csv")

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

            dist_f1 = abs(leader_y - float(row["f1_y"]))
            dist_f2 = abs(leader_y - float(row["f2_y"]))
            dist_f3 = abs(leader_y - float(row["f3_y"]))
            dist_f4 = abs(leader_y - float(row["f4_y"]))

            assert math.isclose(dist_f1, EXPECTED_DIST_INNER, abs_tol=TOLERANCE)
            assert math.isclose(dist_f2, EXPECTED_DIST_INNER, abs_tol=TOLERANCE)
            assert math.isclose(dist_f3, EXPECTED_DIST_OUTER, abs_tol=TOLERANCE)
            assert math.isclose(dist_f4, EXPECTED_DIST_OUTER, abs_tol=TOLERANCE)

    assert valid_frames_tested > 0, (
        "No valid driving frames were found in the safe zone!"
    )


def test_expected_number_of_robots_n5():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, "isaacsim_fleet_data_n5.csv")

    with open(csv_file, mode="r") as file:
        headers = next(csv.reader(file))
        assert len(headers) == 11, (
            f"Expected data for 5 robots, but found {len(headers)} columns."
        )
