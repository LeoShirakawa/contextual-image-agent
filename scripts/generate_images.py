"""Generate product images and brand asset images using Gemini 3 Pro Image, then upload to GCS."""

import base64
import time
from google.cloud import storage
from google import genai
from google.genai import types

PROJECT_ID = "tactile-octagon-372414"
LOCATION = "us-central1"
BUCKET_NAME = "ctx-image-agent-781890406104"

client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
storage_client = storage.Client(project=PROJECT_ID)
bucket = storage_client.bucket(BUCKET_NAME)

PRODUCT_PROMPTS = {
    "P001": "A beautiful Scandinavian dining chair made of natural oak wood, with curved backrest and tapered legs. Product photo on a pure white background, studio lighting, high resolution, transparent background style, PNG.",
    "P002": "A sleek modern floor lamp in matte black steel with a linen fabric shade. Adjustable arm design. Product photo on a pure white background, studio lighting, high resolution, transparent background style, PNG.",
    "P003": "A deep-seated 3-seat sofa in charcoal gray fabric with low profile design and solid wood legs. Contemporary style. Product photo on a pure white background, studio lighting, high resolution, transparent background style, PNG.",
    "P004": "A handcrafted walnut side table with organic live edges and natural wood grain. Small round table. Product photo on a pure white background, studio lighting, high resolution, transparent background style, PNG.",
    "P005": "A minimalist ceramic flower vase in matte white glaze with sculptural organic form. Product photo on a pure white background, studio lighting, high resolution, transparent background style, PNG.",
    "P006": "An open-concept bookshelf in light oak with asymmetric shelving. Modern Scandinavian design. Product photo on a pure white background, studio lighting, high resolution, transparent background style, PNG.",
    "P007": "A hand-dyed indigo blue cushion with shibori pattern. Square throw pillow, cotton and linen blend. Product photo on a pure white background, studio lighting, high resolution, transparent background style, PNG.",
    "P008": "A large rustic dining table made from reclaimed timber with visible knots and grain patterns. Industrial metal trestle base. Product photo on a pure white background, studio lighting, high resolution, transparent background style, PNG.",
    "P009": "A cascading pendant light with multiple hand-blown glass globes in various sizes. Brass hardware and fittings. Product photo on a pure white background, studio lighting, high resolution, transparent background style, PNG.",
    "P010": "A mid-century modern lounge chair in cream leather with chrome steel frame. Elegant curved design. Product photo on a pure white background, studio lighting, high resolution, transparent background style, PNG.",
}

BRAND_ASSET_PROMPTS = {
    "BG001": "Interior photography of a modern minimalist living room. White walls, light hardwood floors, large floor-to-ceiling windows with natural light streaming in. Minimal decor, neutral color palette. Empty space in center for furniture placement. High resolution, professional interior photography.",
    "BG002": "Interior photography of an industrial loft apartment. Exposed red brick walls, polished concrete floor, visible metal pipes and ductwork on high ceilings. Edison bulb string lights. Empty space in center for furniture placement. High resolution, professional interior photography.",
    "BG003": "Interior photography of a bohemian sunroom. Macrame wall hangings, abundant indoor tropical plants, rattan accents, warm golden light streaming through large windows. Earthy tones. Empty space in center for furniture placement. High resolution, professional interior photography.",
    "BG004": "Interior photography of a Japandi style tea room. Tatami-style flooring, shoji screen sliding doors, warm natural wood tones, minimalist garden view through windows, wabi-sabi aesthetic. Empty space in center for furniture placement. High resolution, professional interior photography.",
    "BG005": "Interior photography of a coastal dining room. Whitewashed wood panel walls, large windows with ocean view, natural fiber area rug, sandy warm tones, driftwood accents. Empty space in center for furniture placement. High resolution, professional interior photography.",
}


def generate_and_upload(prompt: str, gcs_path: str) -> bool:
    """Generate an image and upload to GCS."""
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                blob = bucket.blob(gcs_path)
                blob.upload_from_string(image_data, content_type="image/png")
                print(f"  Uploaded: gs://{BUCKET_NAME}/{gcs_path}")
                return True

        print(f"  WARNING: No image generated for {gcs_path}")
        return False
    except Exception as e:
        print(f"  ERROR generating {gcs_path}: {e}")
        return False


def main():
    print("=== Generating Product Images ===")
    for product_id, prompt in PRODUCT_PROMPTS.items():
        gcs_path = f"products/{product_id}.png"
        blob = bucket.blob(gcs_path)
        if blob.exists() and blob.size and blob.size > 100:
            print(f"  Skipping {product_id} (already exists)")
            continue
        print(f"  Generating {product_id}...")
        generate_and_upload(prompt, gcs_path)
        time.sleep(2)

    print("\n=== Generating Brand Asset Images ===")
    for asset_id, prompt in BRAND_ASSET_PROMPTS.items():
        gcs_path = f"brand-assets/{asset_id}.png"
        blob = bucket.blob(gcs_path)
        if blob.exists() and blob.size and blob.size > 100:
            print(f"  Skipping {asset_id} (already exists)")
            continue
        print(f"  Generating {asset_id}...")
        generate_and_upload(prompt, gcs_path)
        time.sleep(2)

    print("\nImage generation complete.")


if __name__ == "__main__":
    main()
