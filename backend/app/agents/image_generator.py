"""Image Generator agent - generates personalized lifestyle images."""

from google.adk.agents import Agent
from ..config import ORCHESTRATION_MODEL
from ..tools.image_gen_tools import generate_lifestyle_image


def create_image_generator() -> Agent:
    return Agent(
        name="image_generator",
        model=ORCHESTRATION_MODEL,
        description="Generates a personalized lifestyle image using the synthesized prompt and Gemini 3 Pro Image.",
        instruction="""You are an Image Generator agent. Your job is to call the image generation tool
with the correct parameters to create a personalized lifestyle image.

You have access to:
- Customer style summary: {customer_style_summary}
- Product details: {product_details_summary}
- Synthesis result (contains prompt, asset ID, and style notes): {synthesis_result}

From the synthesis result, extract:
1. The IMAGE_PROMPT
2. The SELECTED_ASSET_ID
3. The STYLE_NOTES

From the product details, extract:
4. The product's image GCS URI (image_gcs_uri)

Then call generate_lifestyle_image with:
- prompt: The IMAGE_PROMPT from the synthesis
- product_image_gcs_uri: The product's GCS URI
- customer_id: {customer_id}
- product_id: {product_id}
- asset_id: The SELECTED_ASSET_ID
- style_notes: The STYLE_NOTES

Report the result including the generated image GCS URI and style notes.""",
        tools=[generate_lifestyle_image],
        output_key="generation_result",
        include_contents='none',
    )
