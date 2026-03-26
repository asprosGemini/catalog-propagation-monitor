import os
from square import Square
from square.environment import SquareEnvironment


token = os.environ.get("SQUARE_ACCESS_TOKEN")

if not token:
    print("❌ Missing SQUARE_ACCESS_TOKEN env var.")
    raise SystemExit(1)

client = Square(
    environment=SquareEnvironment.SANDBOX,
    token=token,
)


def fetch_catalog_objects():
    objects = list(client.catalog.list())
    print(f"✅ Fetched {len(objects)} catalog objects")

    for obj in objects:
        print(
            f"id={obj.id} | type={obj.type} | version={obj.version}"
        )


if __name__ == "__main__":
    fetch_catalog_objects()