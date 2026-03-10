"""Customer Analyst agent - analyzes customer style preferences."""

from google.adk.agents import Agent
from ..config import ORCHESTRATION_MODEL
from ..tools.bigquery_tools import (
    get_customer_profile,
    get_browsing_history,
    get_purchase_history,
    get_wishlist,
)


def create_customer_analyst() -> Agent:
    return Agent(
        name="customer_analyst",
        model=ORCHESTRATION_MODEL,
        description="Analyzes customer profile, browsing history, purchase history, and wishlist to determine style preferences.",
        instruction="""You are a Customer Style Analyst. Your job is to analyze a customer's data
and produce a concise style preference summary.

The customer_id is available in the session state as {customer_id}.

Steps:
1. Use get_customer_profile to retrieve the customer's profile
2. Use get_browsing_history to see what products they've been looking at
3. Use get_purchase_history to see what they've purchased
4. Use get_wishlist to see what they're interested in

Based on ALL of this data, produce a summary that includes:
- Their primary style preference (e.g. "Modern Minimalist")
- Their preferred color palette
- Key aesthetic keywords that define their taste
- Any patterns you observe from their browsing/purchase behavior

Output a clear, structured summary that will be used by the next agent to select
appropriate background scenes and create an image generation prompt.""",
        tools=[
            get_customer_profile,
            get_browsing_history,
            get_purchase_history,
            get_wishlist,
        ],
        output_key="customer_style_summary",
    )
