"""Create BigQuery dataset, tables, and seed sample data."""

import uuid
import random
from datetime import datetime, timedelta
from google.cloud import bigquery

PROJECT_ID = "tactile-octagon-372414"
DATASET_ID = "contextual_image_agent"
LOCATION = "us-central1"
BUCKET_NAME = "ctx-image-agent-781890406104"

client = bigquery.Client(project=PROJECT_ID)


def create_dataset():
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = LOCATION
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {DATASET_ID} already exists.")
    except Exception:
        client.create_dataset(dataset)
        print(f"Dataset {DATASET_ID} created.")


def create_tables():
    tables = {
        "customers": [
            bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("email", "STRING"),
            bigquery.SchemaField("style_preference", "STRING"),
            bigquery.SchemaField("color_preference", "STRING", mode="REPEATED"),
            bigquery.SchemaField("aesthetic_keywords", "STRING", mode="REPEATED"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
        ],
        "browsing_history": [
            bigquery.SchemaField("history_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "STRING"),
            bigquery.SchemaField("product_id", "STRING"),
            bigquery.SchemaField("viewed_at", "TIMESTAMP"),
            bigquery.SchemaField("duration_seconds", "INT64"),
            bigquery.SchemaField("device", "STRING"),
        ],
        "purchases": [
            bigquery.SchemaField("purchase_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "STRING"),
            bigquery.SchemaField("product_id", "STRING"),
            bigquery.SchemaField("quantity", "INT64"),
            bigquery.SchemaField("price", "FLOAT64"),
            bigquery.SchemaField("purchased_at", "TIMESTAMP"),
        ],
        "wishlists": [
            bigquery.SchemaField("wishlist_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "STRING"),
            bigquery.SchemaField("product_id", "STRING"),
            bigquery.SchemaField("added_at", "TIMESTAMP"),
        ],
        "products": [
            bigquery.SchemaField("product_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("category", "STRING"),
            bigquery.SchemaField("color", "STRING"),
            bigquery.SchemaField("material", "STRING"),
            bigquery.SchemaField("description", "STRING"),
            bigquery.SchemaField("price", "FLOAT64"),
            bigquery.SchemaField("image_gcs_uri", "STRING"),
            bigquery.SchemaField("style_tags", "STRING", mode="REPEATED"),
        ],
        "brand_assets": [
            bigquery.SchemaField("asset_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("scene_name", "STRING"),
            bigquery.SchemaField("description", "STRING"),
            bigquery.SchemaField("style_category", "STRING"),
            bigquery.SchemaField("image_gcs_uri", "STRING"),
        ],
        "generated_images": [
            bigquery.SchemaField("generation_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "STRING"),
            bigquery.SchemaField("product_id", "STRING"),
            bigquery.SchemaField("asset_id", "STRING"),
            bigquery.SchemaField("prompt_used", "STRING"),
            bigquery.SchemaField("image_gcs_uri", "STRING"),
            bigquery.SchemaField("style_notes", "STRING"),
            bigquery.SchemaField("generated_at", "TIMESTAMP"),
        ],
    }

    for table_name, schema in tables.items():
        table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        table = bigquery.Table(table_ref, schema=schema)
        try:
            client.get_table(table_ref)
            print(f"Table {table_name} already exists.")
        except Exception:
            client.create_table(table)
            print(f"Table {table_name} created.")


def seed_customers():
    rows = [
        {
            "customer_id": "C001",
            "name": "Mia Tanaka",
            "email": "mia.tanaka@example.com",
            "style_preference": "Modern Minimalist",
            "color_preference": ["White", "Gray", "Black"],
            "aesthetic_keywords": ["Scandinavian", "Clean", "Simple"],
            "created_at": "2024-03-15T10:00:00Z",
        },
        {
            "customer_id": "C002",
            "name": "Ken Yamada",
            "email": "ken.yamada@example.com",
            "style_preference": "Industrial",
            "color_preference": ["Dark Wood", "Metal", "Black"],
            "aesthetic_keywords": ["Vintage", "Rugged", "Masculine"],
            "created_at": "2024-05-20T14:30:00Z",
        },
        {
            "customer_id": "C003",
            "name": "Hana Sato",
            "email": "hana.sato@example.com",
            "style_preference": "Bohemian",
            "color_preference": ["Terracotta", "Mustard", "Olive"],
            "aesthetic_keywords": ["Natural", "Handmade", "Warm"],
            "created_at": "2024-01-10T09:15:00Z",
        },
        {
            "customer_id": "C004",
            "name": "Ichiro Suzuki",
            "email": "ichiro.suzuki@example.com",
            "style_preference": "Japandi",
            "color_preference": ["Natural Wood", "Indigo", "White"],
            "aesthetic_keywords": ["Japanese", "Traditional", "Zen"],
            "created_at": "2024-07-01T11:00:00Z",
        },
        {
            "customer_id": "C005",
            "name": "Emily Chen",
            "email": "emily.chen@example.com",
            "style_preference": "Coastal Living",
            "color_preference": ["White", "Light Blue", "Sand"],
            "aesthetic_keywords": ["Beach", "Relaxed", "Airy"],
            "created_at": "2024-02-28T16:45:00Z",
        },
    ]
    _insert_rows("customers", rows)


def seed_products():
    rows = [
        {
            "product_id": "P001",
            "name": "Portside Dining Chair",
            "category": "Chair",
            "color": "Natural Oak",
            "material": "Solid Wood",
            "description": "A beautifully crafted dining chair made from sustainably sourced oak. Features a curved backrest and tapered legs for timeless elegance.",
            "price": 349.00,
            "image_gcs_uri": f"gs://{BUCKET_NAME}/products/P001.png",
            "style_tags": ["Scandinavian", "Modern", "Natural"],
        },
        {
            "product_id": "P002",
            "name": "Nordic Floor Lamp",
            "category": "Lighting",
            "color": "Matte Black",
            "material": "Steel/Fabric",
            "description": "Sleek floor lamp with an adjustable arm and linen shade. Provides warm ambient lighting perfect for reading nooks.",
            "price": 249.00,
            "image_gcs_uri": f"gs://{BUCKET_NAME}/products/P002.png",
            "style_tags": ["Nordic", "Minimalist", "Industrial"],
        },
        {
            "product_id": "P003",
            "name": "Haven 3-Seat Sofa",
            "category": "Sofa",
            "color": "Charcoal Gray",
            "material": "Fabric",
            "description": "Deep-seated comfort sofa with removable cushion covers. Low profile design with solid wood legs creates a grounded, contemporary feel.",
            "price": 1499.00,
            "image_gcs_uri": f"gs://{BUCKET_NAME}/products/P003.png",
            "style_tags": ["Modern", "Comfortable", "Versatile"],
        },
        {
            "product_id": "P004",
            "name": "Craft Side Table",
            "category": "Table",
            "color": "Walnut",
            "material": "Solid Wood",
            "description": "Handcrafted walnut side table with organic edges. Each piece is unique with natural wood grain patterns.",
            "price": 219.00,
            "image_gcs_uri": f"gs://{BUCKET_NAME}/products/P004.png",
            "style_tags": ["Artisan", "Natural", "Warm"],
        },
        {
            "product_id": "P005",
            "name": "Bloom Flower Vase",
            "category": "Decor",
            "color": "Ceramic White",
            "material": "Ceramic",
            "description": "Minimalist ceramic vase with a matte white glaze. Sculptural form works as a standalone art piece or with fresh flowers.",
            "price": 65.00,
            "image_gcs_uri": f"gs://{BUCKET_NAME}/products/P005.png",
            "style_tags": ["Minimalist", "Elegant", "Versatile"],
        },
        {
            "product_id": "P006",
            "name": "Harmony Bookshelf",
            "category": "Storage",
            "color": "Light Oak",
            "material": "Plywood/Solid Wood",
            "description": "Open-concept bookshelf with asymmetric shelving. Combines display and storage with a light, airy silhouette.",
            "price": 599.00,
            "image_gcs_uri": f"gs://{BUCKET_NAME}/products/P006.png",
            "style_tags": ["Scandinavian", "Functional", "Modern"],
        },
        {
            "product_id": "P007",
            "name": "Zen Cushion",
            "category": "Textile",
            "color": "Indigo",
            "material": "Cotton/Linen",
            "description": "Hand-dyed indigo cushion using traditional shibori technique. Reversible design with solid linen backing.",
            "price": 52.00,
            "image_gcs_uri": f"gs://{BUCKET_NAME}/products/P007.png",
            "style_tags": ["Japanese", "Artisan", "Traditional"],
        },
        {
            "product_id": "P008",
            "name": "Rustic Dining Table",
            "category": "Table",
            "color": "Reclaimed Wood",
            "material": "Reclaimed Timber",
            "description": "A statement dining table crafted from reclaimed timber with visible knots and grain. Industrial-style metal trestle base.",
            "price": 1199.00,
            "image_gcs_uri": f"gs://{BUCKET_NAME}/products/P008.png",
            "style_tags": ["Industrial", "Rustic", "Sustainable"],
        },
        {
            "product_id": "P009",
            "name": "Cascade Pendant Light",
            "category": "Lighting",
            "color": "Brass",
            "material": "Brass/Glass",
            "description": "Cascading pendant light with hand-blown glass globes in varied sizes. Brass hardware develops a beautiful patina over time.",
            "price": 329.00,
            "image_gcs_uri": f"gs://{BUCKET_NAME}/products/P009.png",
            "style_tags": ["Elegant", "Warm", "Statement"],
        },
        {
            "product_id": "P010",
            "name": "Comfort Lounge Chair",
            "category": "Chair",
            "color": "Cream Leather",
            "material": "Genuine Leather/Steel",
            "description": "Mid-century inspired lounge chair with premium aniline leather upholstery. Chrome steel frame provides a floating appearance.",
            "price": 989.00,
            "image_gcs_uri": f"gs://{BUCKET_NAME}/products/P010.png",
            "style_tags": ["Mid-Century", "Luxury", "Iconic"],
        },
    ]
    _insert_rows("products", rows)


def seed_brand_assets():
    rows = [
        {
            "asset_id": "BG001",
            "scene_name": "Modern Living Room",
            "description": "White walls, hardwood floors, large windows with natural light, minimal decor, neutral palette",
            "style_category": "Modern Minimalist",
            "image_gcs_uri": f"gs://{BUCKET_NAME}/brand-assets/BG001.png",
        },
        {
            "asset_id": "BG002",
            "scene_name": "Industrial Loft",
            "description": "Exposed brick walls, polished concrete floor, metal pipes, high ceilings, Edison bulb lighting",
            "style_category": "Industrial",
            "image_gcs_uri": f"gs://{BUCKET_NAME}/brand-assets/BG002.png",
        },
        {
            "asset_id": "BG003",
            "scene_name": "Bohemian Sunroom",
            "description": "Macrame wall hangings, abundant indoor plants, rattan accents, warm golden light through large windows",
            "style_category": "Bohemian",
            "image_gcs_uri": f"gs://{BUCKET_NAME}/brand-assets/BG003.png",
        },
        {
            "asset_id": "BG004",
            "scene_name": "Japandi Tea Room",
            "description": "Tatami flooring, shoji screen doors, warm wood tones, minimalist garden view, wabi-sabi aesthetic",
            "style_category": "Japandi",
            "image_gcs_uri": f"gs://{BUCKET_NAME}/brand-assets/BG004.png",
        },
        {
            "asset_id": "BG005",
            "scene_name": "Coastal Dining Room",
            "description": "Whitewashed wood panels, ocean-view windows, natural fiber rug, sandy tones, driftwood accents",
            "style_category": "Coastal Living",
            "image_gcs_uri": f"gs://{BUCKET_NAME}/brand-assets/BG005.png",
        },
    ]
    _insert_rows("brand_assets", rows)


def seed_browsing_history():
    # Style-aligned browsing patterns for each customer
    browsing_patterns = {
        "C001": ["P001", "P003", "P005", "P006", "P002", "P001", "P005"],
        "C002": ["P002", "P008", "P010", "P004", "P009", "P008", "P002"],
        "C003": ["P004", "P007", "P009", "P005", "P001", "P007", "P004"],
        "C004": ["P007", "P001", "P004", "P005", "P006", "P007", "P001"],
        "C005": ["P003", "P005", "P006", "P001", "P009", "P010", "P003"],
    }
    devices = ["desktop", "mobile", "tablet"]
    rows = []
    base_date = datetime(2025, 1, 1)

    for cid, products in browsing_patterns.items():
        for i, pid in enumerate(products):
            rows.append({
                "history_id": str(uuid.uuid4())[:8],
                "customer_id": cid,
                "product_id": pid,
                "viewed_at": (base_date + timedelta(days=i * 5, hours=random.randint(8, 22))).isoformat() + "Z",
                "duration_seconds": random.randint(15, 300),
                "device": random.choice(devices),
            })

    _insert_rows("browsing_history", rows)


def seed_purchases():
    purchase_patterns = {
        "C001": [("P001", 349.00), ("P005", 65.00)],
        "C002": [("P008", 1199.00), ("P002", 249.00)],
        "C003": [("P007", 52.00), ("P004", 219.00), ("P009", 329.00)],
        "C004": [("P007", 52.00), ("P001", 349.00)],
        "C005": [("P003", 1499.00), ("P005", 65.00)],
    }
    rows = []
    base_date = datetime(2025, 2, 1)

    for cid, items in purchase_patterns.items():
        for i, (pid, price) in enumerate(items):
            rows.append({
                "purchase_id": str(uuid.uuid4())[:8],
                "customer_id": cid,
                "product_id": pid,
                "quantity": 1,
                "price": price,
                "purchased_at": (base_date + timedelta(days=i * 14)).isoformat() + "Z",
            })

    _insert_rows("purchases", rows)


def seed_wishlists():
    wishlist_patterns = {
        "C001": ["P003", "P006"],
        "C002": ["P010", "P009"],
        "C003": ["P001", "P005", "P003"],
        "C004": ["P004", "P005"],
        "C005": ["P006", "P009", "P010"],
    }
    rows = []
    base_date = datetime(2025, 3, 1)

    for cid, products in wishlist_patterns.items():
        for i, pid in enumerate(products):
            rows.append({
                "wishlist_id": str(uuid.uuid4())[:8],
                "customer_id": cid,
                "product_id": pid,
                "added_at": (base_date + timedelta(days=i * 3)).isoformat() + "Z",
            })

    _insert_rows("wishlists", rows)


def _insert_rows(table_name: str, rows: list[dict]):
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    errors = client.insert_rows_json(table_ref, rows)
    if errors:
        print(f"Error inserting into {table_name}: {errors}")
    else:
        print(f"Inserted {len(rows)} rows into {table_name}.")


if __name__ == "__main__":
    print("=== Setting up BigQuery ===")
    create_dataset()
    create_tables()
    print("\n=== Seeding data ===")
    seed_customers()
    seed_products()
    seed_brand_assets()
    seed_browsing_history()
    seed_purchases()
    seed_wishlists()
    print("\nBigQuery setup complete.")
