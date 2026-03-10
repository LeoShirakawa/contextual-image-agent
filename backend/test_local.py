"""Local test for the Experience Orchestrator agent."""

import asyncio
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "tactile-octagon-372414"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

import importlib
agent_module = importlib.import_module("app.agent")
root_agent = agent_module.root_agent


async def test_agent():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="contextual_image_agent",
        user_id="test_user",
        state={
            "customer_id": "C001",   # Mia Tanaka - Modern Minimalist
            "product_id": "P001",    # Portside Dining Chair
        },
    )

    runner = Runner(
        agent=root_agent,
        app_name="contextual_image_agent",
        session_service=session_service,
    )

    print("=" * 60)
    print("Testing: Customer C001 (Modern Minimalist) + Product P001 (Dining Chair)")
    print("=" * 60)

    message = types.Content(
        role="user",
        parts=[types.Part.from_text(
            text="Generate a personalized lifestyle image for customer C001 viewing product P001."
        )],
    )

    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"\n[{event.author}]: {part.text[:500]}")

    # Check state
    print("\n" + "=" * 60)
    print("Final State Keys:")
    for key in ["customer_style_summary", "product_details_summary", "synthesis_result", "generation_result"]:
        val = session.state.get(key, "NOT SET")
        if val != "NOT SET":
            print(f"  {key}: {str(val)[:200]}...")
        else:
            print(f"  {key}: {val}")

    print("\nTest complete.")


if __name__ == "__main__":
    asyncio.run(test_agent())
