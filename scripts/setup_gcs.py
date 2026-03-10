"""Create GCS bucket for the Contextual Image Agent."""

from google.cloud import storage

PROJECT_ID = "tactile-octagon-372414"
BUCKET_NAME = "ctx-image-agent-781890406104"
LOCATION = "us-central1"


def create_bucket():
    client = storage.Client(project=PROJECT_ID)

    try:
        bucket = client.get_bucket(BUCKET_NAME)
        print(f"Bucket {BUCKET_NAME} already exists.")
    except Exception:
        bucket = client.bucket(BUCKET_NAME)
        bucket.storage_class = "STANDARD"
        bucket = client.create_bucket(bucket, location=LOCATION)
        print(f"Bucket {BUCKET_NAME} created in {LOCATION}.")

    # Create folder placeholders
    for folder in ["products/", "brand-assets/", "generated/"]:
        blob = bucket.blob(folder)
        if not blob.exists():
            blob.upload_from_string("")
            print(f"  Created folder: {folder}")

    print("GCS setup complete.")


if __name__ == "__main__":
    create_bucket()
