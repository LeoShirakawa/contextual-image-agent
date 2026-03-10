"""Image Generator agent - generates personalized lifestyle images via room editing."""

from google.adk.agents import Agent
from ..config import ORCHESTRATION_MODEL
from ..tools.image_gen_tools import generate_lifestyle_image


def create_image_generator() -> Agent:
    return Agent(
        name="image_generator",
        model=ORCHESTRATION_MODEL,
        description="Generates a personalized lifestyle image by editing a room scene to place the product in it using Gemini 3 Pro Image.",
        instruction="""You are an Image Generator agent. Your job is to call the image generation tool
with the correct parameters to edit a room scene and place a product into it.

You have access to:
- Customer style summary: {customer_style_summary}
- Product details: {product_details_summary}
- Synthesis result (contains prompt, asset ID, room image URI, and style notes): {synthesis_result}

From the synthesis result, extract:
1. The IMAGE_PROMPT
2. The SELECTED_ASSET_ID
3. The ROOM_IMAGE_GCS_URI
4. The STYLE_NOTES

From the product details, extract:
5. The product's image GCS URI (image_gcs_uri)

Then call generate_lifestyle_image with:
- prompt: The IMAGE_PROMPT from the synthesis
- product_image_gcs_uri: The product's GCS URI
- room_image_gcs_uri: The ROOM_IMAGE_GCS_URI from the synthesis
- customer_id: {customer_id}
- product_id: {product_id}
- asset_id: The SELECTED_ASSET_ID
- style_notes: The STYLE_NOTES

Report the result including the generated image GCS URI and style notes.""",
        tools=[generate_lifestyle_image],
        output_key="generation_result",
        include_contents='none',
    )
