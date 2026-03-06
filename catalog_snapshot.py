# catalog_snapshot.py
#
# This script fetches catalog objects from the Square Sandbox API and converts them
# into a simplified normalized structure used by the Catalog Propagation Monitor.
#
# The script extracts only the fields needed for propagation monitoring:
# id, type, version, name, price_money, and modifier_list_info.
#
# The result is a list of normalized catalog objects that represent a snapshot
# of the source-of-truth catalog state. This snapshot will later be compared
# against a simulated downstream catalog index to detect propagation mismatches.

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


def extract_name(obj):
    if obj.type == "ITEM" and obj.item_data:
        return obj.item_data.name

    if obj.type == "ITEM_VARIATION" and obj.item_variation_data:
        return obj.item_variation_data.name

    if obj.type == "MODIFIER_LIST" and obj.modifier_list_data:
        return obj.modifier_list_data.name

    if obj.type == "MODIFIER" and obj.modifier_data:
        return obj.modifier_data.name

    return None


def extract_price_money(obj):
    if obj.type == "ITEM_VARIATION" and obj.item_variation_data:
        price = obj.item_variation_data.price_money
        return price.amount if price else None

    if obj.type == "MODIFIER" and obj.modifier_data:
        price = obj.modifier_data.price_money
        return price.amount if price else None

    return None


def extract_modifier_list_info(obj):
    if obj.type == "ITEM" and obj.item_data and obj.item_data.modifier_list_info:
        return [entry.modifier_list_id for entry in obj.item_data.modifier_list_info]

    return []


def normalize_catalog_object(obj):
    return {
        "id": obj.id,
        "type": obj.type,
        "version": obj.version,
        "name": extract_name(obj),
        "price_money": extract_price_money(obj),
        "modifier_list_info": extract_modifier_list_info(obj),
    }


def build_catalog_snapshot():
    snapshot = []

    for obj in client.catalog.list():
        normalized = normalize_catalog_object(obj)
        snapshot.append(normalized)

    return snapshot


if __name__ == "__main__":
    snapshot = build_catalog_snapshot()

    print("✅ Normalized catalog snapshot built successfully!")
    print(f"Total normalized objects: {len(snapshot)}")

    for obj in snapshot:
        print("\n--- Normalized Object ---")
        print(obj)