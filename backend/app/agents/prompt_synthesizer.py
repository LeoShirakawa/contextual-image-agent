"""Prompt Synthesizer agent - creates optimized image editing prompts."""

from google.adk.agents import Agent
from ..config import ORCHESTRATION_MODEL
from ..tools.bigquery_tools import get_brand_assets, list_available_scenes


def create_prompt_synthesizer() -> Agent:
    return Agent(
        name="prompt_synthesizer",
        model=ORCHESTRATION_MODEL,
        description="Synthesizes an optimized image editing prompt by combining customer style preferences, product details, and brand assets.",
        instruction="""You are a Prompt Synthesizer specializing in creating image editing prompts.

You have access to:
- Customer style summary: {customer_style_summary}
- Product details: {product_details_summary}

Steps:
1. Use get_brand_assets with the customer's style preference to find the best matching background scene
2. If no exact match, use list_available_scenes and choose the closest match

Then create a detailed image EDITING prompt. The approach is:
- We have a pre-existing room/background image matching the customer's style
- We have the product image
- Gemini will EDIT the room image to naturally place the product into the scene

The prompt should instruct Gemini to:
- Take the room scene (first image) and place the product (second image) naturally into it
- Maintain the room's existing style, lighting, and atmosphere
- Position the product realistically with proper perspective, shadows, and scale
- Make it look like a professional interior photograph

Output format - provide ALL of the following clearly labeled:
- SELECTED_ASSET_ID: The brand asset ID (e.g. BG001)
- ROOM_IMAGE_GCS_URI: The GCS URI of the selected room background image (from get_brand_assets result, image_gcs_uri field)
- STYLE_NOTES: A brief, customer-friendly description of the personalization (e.g. "Placed in a modern minimalist living room with clean lines and natural light")
- IMAGE_PROMPT: The full detailed prompt for image editing

Example prompt: "Edit the first image (room scene) to naturally place the product shown in the second image into the room. Position the [product name] in [placement details] of the room. Maintain the existing lighting and perspective. Add natural shadows beneath the product. The product should look like it belongs in this [style] room. Professional interior photography quality."
""",
        tools=[
            get_brand_assets,
            list_available_scenes,
        ],
        output_key="synthesis_result",
    )
