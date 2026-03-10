"""Cloud Storage tools for managing images."""

import base64
from google.cloud import storage

from ..config import PROJECT_ID, BUCKET_NAME

_client = None


def _get_client() -> storage.Client:
    global _client
    if _client is None:
        _client = storage.Client(project=PROJECT_ID)
    return _client


def get_product_image_url(product_id: str) -> dict:
    """Gets the public URL for a product image stored in Cloud Storage.

    Args:
        product_id: The product ID (e.g. P001).

    Returns:
        dict with the GCS URI and a signed URL for the product image.
    """
    bucket = _get_client().bucket(BUCKET_NAME)
    blob = bucket.blob(f"products/{product_id}.png")
    if blob.exists():
        gcs_uri = f"gs://{BUCKET_NAME}/products/{product_id}.png"
        return {"status": "success", "gcs_uri": gcs_uri, "product_id": product_id}
    return {"status": "not_found", "product_id": product_id}


def get_image_as_base64(gcs_uri: str) -> dict:
    """Downloads an image from GCS and returns it as base64 encoded data.

    Args:
        gcs_uri: The full GCS URI (e.g. gs://bucket/path/image.png).

    Returns:
        dict with base64 encoded image data.
    """
    parts = gcs_uri.replace("gs://", "").split("/", 1)
    bucket_name = parts[0]
    blob_path = parts[1]

    bucket = _get_client().bucket(bucket_name)
    blob = bucket.blob(blob_path)

    if not blob.exists():
        return {"status": "not_found", "gcs_uri": gcs_uri}

    data = blob.download_as_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    return {"status": "success", "base64_data": b64, "mime_type": "image/png"}


def upload_generated_image(image_base64: str, customer_id: str, product_id: str) -> dict:
    """Uploads a generated image to GCS and returns the URI.

    Args:
        image_base64: Base64 encoded image data.
        customer_id: The customer ID.
        product_id: The product ID.

    Returns:
        dict with the GCS URI of the uploaded image.
    """
    bucket = _get_client().bucket(BUCKET_NAME)
    blob_path = f"generated/{customer_id}_{product_id}.png"
    blob = bucket.blob(blob_path)

    image_data = base64.b64decode(image_base64)
    blob.upload_from_string(image_data, content_type="image/png")

    gcs_uri = f"gs://{BUCKET_NAME}/{blob_path}"
    return {"status": "success", "gcs_uri": gcs_uri}
