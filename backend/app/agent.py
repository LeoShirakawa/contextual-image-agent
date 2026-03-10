"""Root agent definition - Experience Orchestrator."""

from google.adk.agents import SequentialAgent

from .agents.customer_analyst import create_customer_analyst
from .agents.product_analyst import create_product_analyst
from .agents.prompt_synthesizer import create_prompt_synthesizer
from .agents.image_generator import create_image_generator


root_agent = SequentialAgent(
    name="experience_orchestrator",
    description="Orchestrates the personalized image generation pipeline: analyzes customer preferences, retrieves product details, synthesizes a prompt, and generates a lifestyle image.",
    sub_agents=[
        create_customer_analyst(),
        create_product_analyst(),
        create_prompt_synthesizer(),
        create_image_generator(),
    ],
)
