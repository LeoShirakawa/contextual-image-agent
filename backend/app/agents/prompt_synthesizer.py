"""Prompt Synthesizer agent - creates optimized image generation prompts."""

from google.adk.agents import Agent
from ..config import ORCHESTRATION_MODEL
from ..tools.bigquery_tools import get_brand_assets, list_available_scenes


def create_prompt_synthesizer() -> Agent:
    return Agent(
        name="prompt_synthesizer",
        model=ORCHESTRATION_MODEL,
        description="Synthesizes an optimized image generation prompt by combining customer style preferences, product details, and brand assets.",
        instruction="""You are a Prompt Synthesizer specializing in creating image generation prompts.

You have access to:
- Customer style summary: {customer_style_summary}
- Product details: {product_details_summary}

Steps:
1. Use get_brand_assets with the customer's style preference to find the best matching background scene
2. If no exact match, use list_available_scenes and choose the closest match

Then create a detailed, specific image generation prompt that:
- Places the product naturally in the selected background scene
- Incorporates the customer's preferred color palette and aesthetic
- Describes the lighting, mood, and atmosphere matching the customer's style
- Is photorealistic and high quality
- Specifically mentions compositing the product image into the scene

Output format - provide ALL of the following clearly labeled:
- SELECTED_ASSET_ID: The brand asset ID (e.g. BG001)
- STYLE_NOTES: A brief, customer-friendly description of the personalization (e.g. "Placed in a modern minimalist living room with clean lines and natural light")
- IMAGE_PROMPT: The full detailed prompt for image generation

Example prompt: "Create a photorealistic lifestyle image of the [product name] in [color] placed naturally in a [scene description]. The room features [style elements matching customer preference]. Warm natural lighting creates an inviting atmosphere. The [product] is the focal point, positioned [placement details]. Professional interior photography style, high resolution."
""",
        tools=[
            get_brand_assets,
            list_available_scenes,
        ],
        output_key="synthesis_result",
    )
