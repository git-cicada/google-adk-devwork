from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
load_dotenv()

myllm = LiteLlm(model="openai/gpt-4o", temperature=0.5)

# The variable name root_agent is required by ADK to discover the agent. Any other name will not work.
root_agent = Agent(
    model= myllm,
    name="OpenAIAgent",
    description="An agent that uses OpenAI's GPT-4o model to assist with various tasks.",
    instruction="""You are a basic assistant that takes a topic and generates a short social media post about it.
    Keep it concise, relevant, and easy to understand."""
)



#-- OPTIONS TO RUN AGENT --#
# OPTION-1 Use ADK CLI (ADK automatically discovers and runs root_agent from agent.py)
# - From your project root folder, run: adk run openai-agent

# OPTION-2 launch webui : adk web (Run it from Project root folder)

# OPTION-3 Programmatically invoke the agent using the Runner

import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

async def run_agent(topic: str):
    APP_NAME = "openai-agent-app"
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=APP_NAME, user_id="user-123", session_id="session-456") # This is needed even we are it using 'session' explicitiy else will get ValueError: Session not found: session-456 while runnner runs
    runner = Runner(agent = root_agent, app_name=APP_NAME, session_service=session_service)
    message = types.Content(role="user", parts=[types.Part(text=f"Create a short social media post about: {topic}")])

    async for event in runner.run_async(user_id="user-123", session_id="session-456", new_message=message):
        if event.is_final_response():
            print(event.content.parts[0].text)
            break
        

if __name__ == "__main__":
    topic = "The benefits of drinking lemon water daily."
    asyncio.run(run_agent(topic))