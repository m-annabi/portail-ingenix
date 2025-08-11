from __future__ import annotations
from typing import List
from .bsp import Vec3, Polygon, BSPTree, make_cube
import math


def distance(a: Vec3, b: Vec3) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def apply_explosion(tree: BSPTree, position: Vec3, radius: float) -> BSPTree:
    """Remove polygons whose centroid lies within the explosion radius."""
    remaining: List[Polygon] = []
    for poly in tree.all_polygons():
        if distance(poly.centroid(), position) > radius:
            remaining.append(poly)
    return BSPTree(remaining)


def build_city(rows: int, cols: int, spacing: float, size: float) -> BSPTree:
    """Create a simple grid of cube buildings."""
    polys: List[Polygon] = []
    for i in range(rows):
        for j in range(cols):
            center = Vec3(i * spacing, 0, j * spacing)
            polys.extend(make_cube(center, size))
    return BSPTree(polys)
