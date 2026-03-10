"""BigQuery tools for querying customer and product data."""

from google.cloud import bigquery
from google.adk.tools import ToolContext

from ..config import PROJECT_ID, DATASET_ID

_client = None


def _get_client() -> bigquery.Client:
    global _client
    if _client is None:
        _client = bigquery.Client(project=PROJECT_ID)
    return _client


def _query(sql: str) -> list[dict]:
    result = _get_client().query(sql).result()
    rows = []
    for row in result:
        r = dict(row)
        for k, v in r.items():
            if hasattr(v, "isoformat"):
                r[k] = v.isoformat()
        rows.append(r)
    return rows


def get_customer_profile(customer_id: str) -> dict:
    """Retrieves the customer profile including style preferences, color preferences, and aesthetic keywords.

    Args:
        customer_id: The customer ID (e.g. C001).

    Returns:
        dict with customer profile data.
    """
    rows = _query(f"""
        SELECT customer_id, name, email, style_preference,
               color_preference, aesthetic_keywords
        FROM `{PROJECT_ID}.{DATASET_ID}.customers`
        WHERE customer_id = '{customer_id}'
    """)
    if rows:
        return {"status": "success", "customer": rows[0]}
    return {"status": "not_found", "customer_id": customer_id}


def get_browsing_history(customer_id: str) -> dict:
    """Retrieves the recent browsing history for a customer, showing which products they viewed and for how long.

    Args:
        customer_id: The customer ID (e.g. C001).

    Returns:
        dict with browsing history records.
    """
    rows = _query(f"""
        SELECT bh.product_id, p.name as product_name, p.category, p.style_tags,
               bh.viewed_at, bh.duration_seconds, bh.device
        FROM `{PROJECT_ID}.{DATASET_ID}.browsing_history` bh
        JOIN `{PROJECT_ID}.{DATASET_ID}.products` p ON bh.product_id = p.product_id
        WHERE bh.customer_id = '{customer_id}'
        ORDER BY bh.viewed_at DESC
        LIMIT 20
    """)
    return {"status": "success", "history": rows, "count": len(rows)}


def get_purchase_history(customer_id: str) -> dict:
    """Retrieves the purchase history for a customer, showing what products they have bought.

    Args:
        customer_id: The customer ID (e.g. C001).

    Returns:
        dict with purchase records.
    """
    rows = _query(f"""
        SELECT pu.product_id, p.name as product_name, p.category,
               p.style_tags, pu.price, pu.purchased_at
        FROM `{PROJECT_ID}.{DATASET_ID}.purchases` pu
        JOIN `{PROJECT_ID}.{DATASET_ID}.products` p ON pu.product_id = p.product_id
        WHERE pu.customer_id = '{customer_id}'
        ORDER BY pu.purchased_at DESC
    """)
    return {"status": "success", "purchases": rows, "count": len(rows)}


def get_wishlist(customer_id: str) -> dict:
    """Retrieves the wishlist items for a customer.

    Args:
        customer_id: The customer ID (e.g. C001).

    Returns:
        dict with wishlist items.
    """
    rows = _query(f"""
        SELECT w.product_id, p.name as product_name, p.category,
               p.style_tags, w.added_at
        FROM `{PROJECT_ID}.{DATASET_ID}.wishlists` w
        JOIN `{PROJECT_ID}.{DATASET_ID}.products` p ON w.product_id = p.product_id
        WHERE w.customer_id = '{customer_id}'
        ORDER BY w.added_at DESC
    """)
    return {"status": "success", "wishlist": rows, "count": len(rows)}


def get_product_details(product_id: str) -> dict:
    """Retrieves full product details including name, category, color, material, description, price, and style tags.

    Args:
        product_id: The product ID (e.g. P001).

    Returns:
        dict with product details.
    """
    rows = _query(f"""
        SELECT product_id, name, category, color, material,
               description, price, image_gcs_uri, style_tags
        FROM `{PROJECT_ID}.{DATASET_ID}.products`
        WHERE product_id = '{product_id}'
    """)
    if rows:
        return {"status": "success", "product": rows[0]}
    return {"status": "not_found", "product_id": product_id}


def get_all_products() -> dict:
    """Retrieves all products from the catalog.

    Returns:
        dict with list of all products.
    """
    rows = _query(f"""
        SELECT product_id, name, category, color, material,
               description, price, image_gcs_uri, style_tags
        FROM `{PROJECT_ID}.{DATASET_ID}.products`
        ORDER BY product_id
    """)
    return {"status": "success", "products": rows, "count": len(rows)}


def get_brand_assets(style_category: str) -> dict:
    """Retrieves brand assets (background scenes) matching a style category.

    Args:
        style_category: The style category to match (e.g. Modern Minimalist, Industrial, Bohemian, Japandi, Coastal Living).

    Returns:
        dict with matching brand assets.
    """
    rows = _query(f"""
        SELECT asset_id, scene_name, description, style_category, image_gcs_uri
        FROM `{PROJECT_ID}.{DATASET_ID}.brand_assets`
        WHERE style_category = '{style_category}'
    """)
    if rows:
        return {"status": "success", "assets": rows}
    # Fallback: return all assets
    rows = _query(f"""
        SELECT asset_id, scene_name, description, style_category, image_gcs_uri
        FROM `{PROJECT_ID}.{DATASET_ID}.brand_assets`
    """)
    return {"status": "success", "assets": rows, "note": "No exact match, returning all assets"}


def list_available_scenes() -> dict:
    """Lists all available background scene assets with their style categories.

    Returns:
        dict with all available scenes.
    """
    rows = _query(f"""
        SELECT asset_id, scene_name, description, style_category
        FROM `{PROJECT_ID}.{DATASET_ID}.brand_assets`
        ORDER BY asset_id
    """)
    return {"status": "success", "scenes": rows}
