# catalog_seed.py creates a demo item with modifiers in the Square Sandbox catalog so our monitoring tool has real catalog objects to track.
# The script uses the Square API to create a test product (pizza) with modifiers (cheese, pepperoni, mushrooms) and sends them to the Sandbox catalog using a batch API request.

import os
import uuid
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

def new_idempotency_key() -> str:
    return str(uuid.uuid4())

# Use "client-side IDs" (start with #) so Square maps them to real IDs.
modifier_list_client_id = f"#MOD_LIST_{uuid.uuid4().hex[:8]}"

modifier_list = {
    "type": "MODIFIER_LIST",
    "id": modifier_list_client_id,
    "modifier_list_data": {
        "name": "Toppings (Demo)",
        "selection_type": "MULTIPLE",
        "modifiers": [
            {
                "type": "MODIFIER",
                "id": f"#MOD_{uuid.uuid4().hex[:8]}",
                "modifier_data": {
                    "name": "Cheese",
                    "price_money": {"amount": 0, "currency": "USD"},
                },
            },
            {
                "type": "MODIFIER",
                "id": f"#MOD_{uuid.uuid4().hex[:8]}",
                "modifier_data": {
                    "name": "Pepperoni",
                    "price_money": {"amount": 100, "currency": "USD"},
                },
            },
            {
                "type": "MODIFIER",
                "id": f"#MOD_{uuid.uuid4().hex[:8]}",
                "modifier_data": {
                    "name": "Mushrooms",
                    "price_money": {"amount": 75, "currency": "USD"},
                },
            },
        ],
    },
}

item_client_id = f"#ITEM_{uuid.uuid4().hex[:8]}"
variation_client_id = f"#VAR_{uuid.uuid4().hex[:8]}"

item = {
    "type": "ITEM",
    "id": item_client_id,
    "item_data": {
        "name": "Test Pizza (Demo)",
        "description": "Demo item for Catalog Propagation Monitor",
        "variations": [
            {
                "type": "ITEM_VARIATION",
                "id": variation_client_id,
                "item_variation_data": {
                    "name": "Regular",
                    "pricing_type": "FIXED_PRICING",
                    "price_money": {"amount": 1299, "currency": "USD"},
                },
            }
        ],
        # Attach the modifier list to the item
        "modifier_list_info": [
            {"modifier_list_id": modifier_list_client_id, "enabled": True}
        ],
    },
}

print("Seeding catalog objects into Sandbox...")

resp = client.catalog.batch_upsert(
    idempotency_key=new_idempotency_key(),
    batches=[
        {
            "objects": [
                modifier_list,
                item,
            ]
        }
    ],
)

# The SDK returns a response object; errors will be present if something went wrong.
errors = getattr(resp, "errors", None)
if errors:
    print("❌ Errors creating catalog objects:")
    for e in errors:
        print(e)
    raise SystemExit(1)

print("✅ Seeded catalog objects successfully!")

id_mappings = getattr(resp, "id_mappings", None) or []
print("\nID mappings (client IDs -> real object IDs):")
for m in id_mappings:
    # Different SDK versions may represent mappings slightly differently
    client_id = getattr(m, "client_object_id", None) or getattr(m, "client_object_id", "")
    obj_id = getattr(m, "object_id", None) or getattr(m, "object_id", "")
    print(f"- {client_id} -> {obj_id}")

print("\nDone.")