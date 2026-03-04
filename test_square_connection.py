import os
from square import Square
from square.environment import SquareEnvironment

token = os.environ.get("SQUARE_ACCESS_TOKEN")

if not token:
    print("❌ No access token found. Make sure SQUARE_ACCESS_TOKEN is set.")
    raise SystemExit(1)

client = Square(
    environment=SquareEnvironment.SANDBOX,
    token=token,
)

# Simple “hello world” call (locations exist by default in sandbox)
response = client.locations.list()

print("✅ Connected to Square Sandbox successfully!")
for loc in response.locations:
    print(f"- {loc.id} | {loc.name}")