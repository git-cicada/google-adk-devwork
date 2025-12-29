import uuid
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
load_dotenv()

# Define LLM
llm = LiteLlm(model="openai/gpt-4o-mini", temperature=0)

root_agent = Agent(
    name="SessionAgent",
    model=llm,
    description="An agent that demonstrates session handling using Google ADK.",
    instruction="User's favourite colour is {favorite_color}, name {name}, and favourite food: {favorite_food}. Answer questions about it."
)

session_service = InMemorySessionService()
session_id = str(uuid.uuid4())
APP_NAME = "session-agent-app"
USER_ID = "user-123"

# Create a new session
session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=session_id,
    state={"name": "Bob", "favorite_color": "blue", "favorite_food": "pizza"} #Intial State
)

# Agent Runner
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

# User Message
user_message = types.Content(
    role="user",
    parts=[types.Part(text="What is Bob's favorite color and food?")]
)

for event in runner.run(
    user_id=USER_ID,
    session_id=session_id,
    new_message=user_message
):
    if event.is_final_response() and event.content and event.content.parts:
        print(event.content.parts[0].text)
        print("-----------------------")
        break

# What Happens when runner.run is called?
"""
#------
1. Runner retrieves session by user_id, session_id
2. Fills placeholders in the prompt with state (green, Vaibhav Mehra, Mathematics)
3. Calls Gemini - our base LLM
4. Outputs a response
#------
"""

# # Now manually fetch the session from memory so we can inspect its state. 
session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)

# # 6️⃣ Print updated state
print("\n📘 Final session state:")
for key, value in session.state.items():
    print(f"{key}: {value}")


# NOTE: If we ask the model to update the session state, the model can’t modify the state by itself! So we need a way to be able to parse it!

