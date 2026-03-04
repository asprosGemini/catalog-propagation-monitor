import os
from square import Square
from square.environment import SquareEnvironment

token = os.environ.get("SQUARE_ACCESS_TOKEN")

client = Square(
    environment=SquareEnvironment.SANDBOX,
    token=token,
)

print("Fetching catalog objects...\n")

count = 0

for obj in client.catalog.list():
    count += 1
    print("\n--- Catalog Object ---")
    print(f"ID: {obj.id}")
    print(f"Type: {obj.type}")
    print(f"Version: {obj.version}")

print(f"\nTotal catalog objects found: {count}")