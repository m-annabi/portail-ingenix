from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import math


@dataclass
class Vec3:
    """Simple 3D vector class with basic operations."""
    x: float
    y: float
    z: float

    def __add__(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vec3':
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    __rmul__ = __mul__

    def dot(self, other: 'Vec3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vec3') -> 'Vec3':
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        return math.sqrt(self.dot(self))

    def normalize(self) -> 'Vec3':
        l = self.length()
        if l == 0:
            return Vec3(0, 0, 0)
        return self * (1.0 / l)


@dataclass
class Plane:
    normal: Vec3
    d: float

    @classmethod
    def from_points(cls, a: Vec3, b: Vec3, c: Vec3) -> 'Plane':
        ab = b - a
        ac = c - a
        n = ab.cross(ac).normalize()
        d = n.dot(a)
        return cls(n, d)

    def classify_point(self, p: Vec3, eps: float = 1e-5) -> float:
        return self.normal.dot(p) - self.d


@dataclass
class Polygon:
    vertices: List[Vec3]
    plane: Plane

    @classmethod
    def from_vertices(cls, verts: List[Vec3]) -> 'Polygon':
        if len(verts) < 3:
            raise ValueError("Polygon needs at least 3 vertices")
        plane = Plane.from_points(verts[0], verts[1], verts[2])
        return cls(verts, plane)

    def centroid(self) -> Vec3:
        x = sum(v.x for v in self.vertices) / len(self.vertices)
        y = sum(v.y for v in self.vertices) / len(self.vertices)
        z = sum(v.z for v in self.vertices) / len(self.vertices)
        return Vec3(x, y, z)


class BSPNode:
    """Node of a BSP tree. This implementation is minimal and only stores polygons."""
    def __init__(self, polygons: Optional[List[Polygon]] = None):
        self.plane: Optional[Plane] = None
        self.front: Optional[BSPNode] = None
        self.back: Optional[BSPNode] = None
        self.polygons: List[Polygon] = []
        if polygons:
            self.build(polygons)

    def build(self, polygons: List[Polygon]):
        if not polygons:
            return
        if not self.plane:
            self.plane = polygons[0].plane
        coplanar: List[Polygon] = []
        front: List[Polygon] = []
        back: List[Polygon] = []
        for poly in polygons:
            classification = self.plane.classify_point(poly.centroid())
            if abs(classification) <= 1e-5:
                coplanar.append(poly)
            elif classification > 0:
                front.append(poly)
            else:
                back.append(poly)
        self.polygons.extend(coplanar)
        if front:
            if not self.front:
                self.front = BSPNode()
            self.front.build(front)
        if back:
            if not self.back:
                self.back = BSPNode()
            self.back.build(back)


class BSPTree:
    def __init__(self, polygons: List[Polygon]):
        self.root = BSPNode(polygons)

    def all_polygons(self) -> List[Polygon]:
        result: List[Polygon] = []

        def traverse(node: Optional[BSPNode]):
            if not node:
                return
            result.extend(node.polygons)
            traverse(node.front)
            traverse(node.back)

        traverse(self.root)
        return result


# Helper functions to create geometry

def make_cube(center: Vec3, size: float) -> List[Polygon]:
    cx, cy, cz = center.x, center.y, center.z
    s = size / 2.0
    pts = [
        Vec3(cx - s, cy - s, cz - s),
        Vec3(cx + s, cy - s, cz - s),
        Vec3(cx + s, cy + s, cz - s),
        Vec3(cx - s, cy + s, cz - s),
        Vec3(cx - s, cy - s, cz + s),
        Vec3(cx + s, cy - s, cz + s),
        Vec3(cx + s, cy + s, cz + s),
        Vec3(cx - s, cy + s, cz + s),
    ]
    # faces
    faces = [
        [pts[0], pts[1], pts[2], pts[3]],  # back
        [pts[4], pts[5], pts[6], pts[7]],  # front
        [pts[0], pts[1], pts[5], pts[4]],  # bottom
        [pts[2], pts[3], pts[7], pts[6]],  # top
        [pts[1], pts[2], pts[6], pts[5]],  # right
        [pts[3], pts[0], pts[4], pts[7]],  # left
    ]
    return [Polygon.from_vertices(f) for f in faces]
