"""Deploy the Contextual Image Agent to Agent Engine (Vertex AI)."""

import os
import json
import vertexai
from vertexai import agent_engines

PROJECT_ID = "tactile-octagon-372414"
LOCATION = "us-central1"

os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=f"gs://ctx-image-agent-781890406104",
)


def deploy():
    print("Deploying Contextual Image Agent to Agent Engine...")

    from app.agent import root_agent

    agent_engine = agent_engines.create(
        agent_engine=root_agent,
        requirements=[
            "google-adk>=1.0.0",
            "google-cloud-bigquery>=3.25.0",
            "google-cloud-storage>=2.18.0",
            "google-genai>=1.0.0",
        ],
        display_name="contextual-image-agent",
        description="Multi-agent system for personalized product image generation",
        extra_packages=[],
        env_vars={
            "GOOGLE_CLOUD_LOCATION": "global",
            "GOOGLE_GENAI_USE_VERTEXAI": "True",
        },
    )

    resource_name = agent_engine.resource_name
    resource_id = resource_name.split("/")[-1]

    print(f"\nDeployment successful!")
    print(f"Resource Name: {resource_name}")
    print(f"Resource ID: {resource_id}")

    metadata = {
        "remote_agent_engine_id": resource_name,
        "resource_id": resource_id,
        "deployment_target": "agent_engine",
        "project_id": PROJECT_ID,
        "location": LOCATION,
    }

    with open("deployment_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nMetadata saved to deployment_metadata.json")
    print(f"\nTo query this agent:")
    print(f'  agent = agent_engines.get("{resource_name}")')
    print(f'  session = await agent.async_create_session(user_id="test")')
    print(f'  async for event in agent.async_stream_query(user_id="test", session_id=session["id"], message="..."):')
    print(f"      print(event)")

    return agent_engine


if __name__ == "__main__":
    deploy()
