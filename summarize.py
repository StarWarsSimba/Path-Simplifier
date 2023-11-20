"""Summarize a path in a map, using the standard Ramer-Douglas-Peucher (aka Duda-Hart)
split-and-merge algorithm.
Author: Your name here
Credits: TBD
"""

import csv
import doctest
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

import geometry
import map_view
import config


def read_points(path: str) -> list[tuple[float, float]]:
    coord_pairs = []
    with open(path, newline="") as source_file:
        reader = csv.DictReader(source_file)
        for row in reader:
            easting = float(row["Easting"])
            northing = float(row["Northing"])
            coord_pairs.append((easting, northing))
    return coord_pairs


def summarize(points: list[tuple[float, float]],
              tolerance: int = config.TOLERANCE_METERS,
              ) -> list[tuple[float, float]]:
    """
    #>>> path = [(0, 0), (1, 1), (2, 2), (2, 3), (2, 4), (3, 4), (4, 4)]
    #>>> expect = [(0, 0), (2, 2), (2, 4), (4, 4)]
    #>>> simple = summarize(path, tolerance=0.5)
    #>>> simple == expect
    #True
    """
    summary: list[tuple[float, float]] = [points[0]]
    epsilon = float(tolerance * tolerance)

    def simplify(start: int, end: int):
        """Add necessary points in (start, end) to summary."""
        log.debug(f"Simplifying from {start}: {points[start]} to {end}: {points[end]}, {points[start + 1:end]}")
        log.debug(f"Summary so far: {summary}")
        map_view.scratch(points[start], points[end])
        p = (0, 0)
        p_index = 0
        max_distance = 0
        for i in range(start, end):
            distance = geometry.deviation_sq(points[0], points[-1], points[i])
            if distance > tolerance:
                if distance > max_distance:
                    max_distance = distance
                    p = points[i]
                    p_index = i
        summary.append(p)
        simplify(start, p_index)
        simplify(p_index, end)
        return

    simplify(0, len(points) - 1)
    return summary


def main():
    points = read_points(config.UTM_CSV)
    for point in points:
        map_view.plot_to(point)
    map_view.init()
    print(f"{len(points)} raw points")
    summary = summarize(points, config.TOLERANCE_METERS)
    print(f"{len(summary)} points in summary")
    map_view.wait_to_close()


if __name__ == "__main__":
    doctest.testmod()
    print("Tested")
    main()