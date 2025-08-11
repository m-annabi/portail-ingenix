from engine import build_city, apply_explosion, Vec3


def main():
    city = build_city(rows=3, cols=3, spacing=20.0, size=10.0)
    print("Initial polygons:", len(city.all_polygons()))
    city = apply_explosion(city, Vec3(20.0, 0.0, 20.0), radius=12.0)
    print("Polygons after explosion:", len(city.all_polygons()))


if __name__ == "__main__":
    main()
