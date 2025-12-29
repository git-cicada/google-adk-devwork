import uuid
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
from pydantic import BaseModel, Field
load_dotenv()

# Define LLM
llm = LiteLlm(model="openai/gpt-4o-mini", temperature=0)


# Defining our schema using pydantic
class StateOutput(BaseModel):
    favorite_color: str    = Field(description="Favourite colour of user.")
    name:      str    = Field(description="Name of the user.")
    favorite_food: str  = Field(description="Favourite food of the user.")



root_agent = Agent(
    name="SessionAgent",
    model=llm,
    description="An agent that demonstrates session handling using Google ADK.",
    output_schema=StateOutput,
    output_key="state",
    disallow_transfer_to_parent=True, #(TO avoid error Invalid config for agent SessionAgent: output_schema cannot co-exist with agent transfer configurations.)
    disallow_transfer_to_peers=True,
    instruction="""
You are a helpful assistant that knows the user's name, favorite colour, and favorite food.

Current state:
- name: {name}
- favorite_color: {favorite_color}
- favorite_food: {favorite_food}

If the user asks to update anything, reply *only* with JSON matching this schema: 

{
  "favorite_color": "<new colour>",
  "name": "<new name>",
  "favorite_food": "<new food>"
}

When updating, preserve existing values for fields that should remain the same. Only change the specific fields mentioned by the user.

Otherwise, answer their question in plain text.
""")

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


def user_message(usr_msg: str):
     return types.Content(
        role="user",
        parts=[types.Part(text=usr_msg)]
    )

def read_the_session_state() -> None:
    session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    print("\n📘 Final session state:")
    for key, value in session.state.items():
        print(f"{key}: {value}")

def agent_runner(runner, USER_ID, session_id, usr_msg):
    for event in runner.run(
        user_id=USER_ID,
        session_id=session_id,
        new_message=user_message(usr_msg)
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)
            print("-----------------------")
            # break


if __name__ == "__main__":
    # Agent Runner
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)   
    
    # # Initial Query
    usr_msg = "What is Bob's favorite color and food?"
    agent_runner(runner, USER_ID, session_id, usr_msg)
    read_the_session_state()

    # Update Query
    update_msg = "Change my favorite color to green and my favorite food to sushi."
    agent_runner(runner, USER_ID, session_id, update_msg)
    read_the_session_state()

    # Verify Update
    verify_msg = "What is my favorite color and food now?"
    agent_runner(runner, USER_ID, session_id, verify_msg)
    read_the_session_state()




