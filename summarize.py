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


def main():
    points = read_points(config.UTM_CSV)
    for point in points:
        map_view.plot_to(point)
    map_view.init()
    map_view.wait_to_close()
if __name__ == "__main__":
    doctest.testmod()
    print("Tested")
    main()