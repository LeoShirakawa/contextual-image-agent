"""Image generation tool using Gemini 3 Pro Image - room editing approach."""

import uuid
from datetime import datetime, timezone

from google import genai
from google.genai import types
from google.cloud import storage, bigquery

from ..config import PROJECT_ID, LOCATION, BUCKET_NAME, DATASET_ID, IMAGE_MODEL

_genai_client = None
_storage_client = None
_bq_client = None


def _get_genai_client():
    global _genai_client
    if _genai_client is None:
        _genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    return _genai_client


def _get_storage_client():
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client(project=PROJECT_ID)
    return _storage_client


def _get_bq_client():
    global _bq_client
    if _bq_client is None:
        _bq_client = bigquery.Client(project=PROJECT_ID)
    return _bq_client


def _download_gcs_image(gcs_uri: str) -> bytes | None:
    """Download an image from GCS and return its bytes."""
    storage_c = _get_storage_client()
    parts = gcs_uri.replace("gs://", "").split("/", 1)
    bucket = storage_c.bucket(parts[0])
    blob = bucket.blob(parts[1])
    if blob.exists():
        return blob.download_as_bytes()
    return None


def generate_lifestyle_image(
    prompt: str,
    product_image_gcs_uri: str,
    room_image_gcs_uri: str,
    customer_id: str,
    product_id: str,
    asset_id: str,
    style_notes: str,
) -> dict:
    """Generates a personalized lifestyle image by editing a room scene to place a product in it using Gemini 3 Pro Image.

    This tool takes a pre-existing room/background image and a product image,
    then uses Gemini to edit the room scene by naturally placing the product into it.

    Args:
        prompt: The detailed image editing prompt describing how to place the product in the room.
        product_image_gcs_uri: GCS URI of the product image to place in the room.
        room_image_gcs_uri: GCS URI of the room/background scene image to edit.
        customer_id: The customer ID for whom this image is being generated.
        product_id: The product ID being visualized.
        asset_id: The brand asset ID used for the background scene.
        style_notes: Brief description of the personalization applied.

    Returns:
        dict with the generated image GCS URI and style notes.
    """
    client = _get_genai_client()

    # Download both images
    room_image_bytes = _download_gcs_image(room_image_gcs_uri)
    product_image_bytes = _download_gcs_image(product_image_gcs_uri)

    if room_image_bytes is None:
        return {"status": "error", "message": f"Room image not found: {room_image_gcs_uri}"}
    if product_image_bytes is None:
        return {"status": "error", "message": f"Product image not found: {product_image_gcs_uri}"}

    # Build the request: room image + product image + editing prompt
    contents = [
        types.Part(
            inline_data=types.Blob(mime_type="image/png", data=room_image_bytes)
        ),
        types.Part(
            inline_data=types.Blob(mime_type="image/png", data=product_image_bytes)
        ),
        types.Part.from_text(text=prompt),
    ]

    try:
        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        image_data = None
        response_text = ""

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
            elif part.text is not None:
                response_text = part.text

        if image_data is None:
            return {"status": "error", "message": "No image was generated", "model_response": response_text}

        # Upload to GCS
        gen_blob_path = f"generated/{customer_id}_{product_id}.png"

        storage_c = _get_storage_client()
        upload_bucket = storage_c.bucket(BUCKET_NAME)
        upload_blob = upload_bucket.blob(gen_blob_path)
        upload_blob.upload_from_string(image_data, content_type="image/png")

        gcs_uri = f"gs://{BUCKET_NAME}/{gen_blob_path}"

        # Record in BigQuery
        generation_id = str(uuid.uuid4())[:8]
        row = {
            "generation_id": generation_id,
            "customer_id": customer_id,
            "product_id": product_id,
            "asset_id": asset_id,
            "prompt_used": prompt[:4000],
            "image_gcs_uri": gcs_uri,
            "style_notes": style_notes,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        table_ref = f"{PROJECT_ID}.{DATASET_ID}.generated_images"
        _get_bq_client().insert_rows_json(table_ref, [row])

        return {
            "status": "success",
            "image_gcs_uri": gcs_uri,
            "style_notes": style_notes,
            "generation_id": generation_id,
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
