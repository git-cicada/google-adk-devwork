from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
# from google.adk.tools import google_search # Does not work with openai/gpt-4o model
from dotenv import load_dotenv
load_dotenv()

def get_contact(person: str) -> dict:
    """
    Argument:
        person: Name of the person to get contact information for.
    Returns:
        A dictionary containing the contact information of the person.
        Example: {"Bob:"12345}

    """
    lookup = {
    "Alice": "111-222-3333",
    "Bob": "123-456-7890",
    "Charlie": "987-654-3210",
    "Angela": "555-666-7777"
    }

    return {person: lookup.get(person, "Contact not found")}

root_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o", temperature=0.5),
    name="BasicToolAgent",
    description="An agent that uses OpenAI's GPT-4o model to assist with various tasks.",
    instruction="""You are a basic assistant that takes the user input and answers using the available tools if needed.""",
    tools=[get_contact]
)