import xml.etree.ElementTree as ET
from math import acos, degrees
from collections import defaultdict
from sys import stdout

import numpy as np


def calc_sphere(x, y, z):
    """Calculate spherical coordinates for axial data."""
    return np.degrees(np.arctan2(*(np.array((
        x, y)) * np.sign(z)))) % 360, np.degrees(np.arccos(np.abs(z)))


def parse_pp(fname, start, end):
    tree = ET.parse(fname)
    points = defaultdict(list)
    for x in tree.getroot().findall("./point"):
        points[x.attrib["name"]].append(
            np.array((float(x.attrib['x']), float(x.attrib['y']), float(
                x.attrib['z']))))

    scanline_start = points.pop(start)[0]
    scanline_vector = points.pop(end)[0] - scanline_start
    scanline_vector /= np.linalg.norm(scanline_vector)

    points_data = []
    for point in points:
        a, b, c = points[point]
        ab = b - a
        ac = c - a
        bc = c - b
        length = max([np.linalg.norm(x) for x in (ab, ac, bc)])
        centroid = np.mean((a, b, c), axis=0)
        d = np.dot(centroid - scanline_start, scanline_vector)
        n = np.cross(ab, ac)
        n /= np.linalg.norm(n)
        angle = degrees(acos(abs(np.dot(n, scanline_vector))))
        theta, phi = calc_sphere(*n)
        points_data.append([theta, phi, point, d, length, angle])
    points_data.sort(key=lambda point: point[3])
    return points_data

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Process .pp files into scanline data.")
    parser.add_argument(
        "--start",
        action="store",
        dest="start",
        default="S1",
        help="name of point at start of scanline")
    parser.add_argument(
        "--end",
        action="store",
        dest="end",
        default="S2",
        help="name of point at end of scanline")
    parser.add_argument(
        "--out",
        action="store",
        dest="out",
        default=None,
        help="name of output file, prints to stdout if not given")
    parser.add_argument(
        "fname",
        action="store",
        help="input .pp file from meshlab's point picking tool")
    args = parser.parse_args()
    data = parse_pp(args.fname, args.start, args.end)
    if args.out is None:
        f = stdout
    else:
        f = open(args.out, "wb")
    from csv import writer
    data_writer = writer(f)
    data_writer.writerow(
        ["#dipdir", "dip", "point", "position", "length", "angle"])
    data_writer.writerows(data)
    if args.out is not None:
        f.close()

if __name__ == "__main__":
    main()
