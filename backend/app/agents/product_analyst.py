"""Product Analyst agent - retrieves product details."""

from google.adk.agents import Agent
from ..config import ORCHESTRATION_MODEL
from ..tools.bigquery_tools import get_product_details
from ..tools.storage_tools import get_product_image_url


def create_product_analyst() -> Agent:
    return Agent(
        name="product_analyst",
        model=ORCHESTRATION_MODEL,
        description="Retrieves and analyzes product details including name, color, material, and image location.",
        instruction="""You are a Product Analyst. Your job is to retrieve complete details about the product
the customer is currently viewing.

The product_id is available in the session state as {product_id}.

Steps:
1. Use get_product_details to get the full product information
2. Use get_product_image_url to confirm the product image is available in GCS

Produce a structured summary of the product including:
- Product name, category, color, material
- Product description
- Style tags
- The GCS URI for the product image (important for image generation)

This information will be used to create a personalized lifestyle image.""",
        tools=[
            get_product_details,
            get_product_image_url,
        ],
        output_key="product_details_summary",
    )
