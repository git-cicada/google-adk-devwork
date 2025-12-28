from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()

llm = LiteLlm(model="openai/gpt-4o", temperature=0.5)

class StructuredOutput(BaseModel):
    title: str = Field(..., description="The title of the output")
    description: str = Field(..., description="A detailed description")
    tags: list[str] = Field(..., description="A list of relevant tags")

root_agent = Agent(
    model=llm,
    name="StructuredAgent",
    description="An agent that uses OpenAI's GPT-4o model to assist with structured tasks.",
    instruction="""You are a structured assistant that takes user input and generates structured outputs based on formats
    Ensure that the outputs in a json object like {\"title\": \"AI Vs Human\", \"description\": \"AI and Human...\", \"tags\": [\"AI\", \"Human\"]}""",
    output_schema=StructuredOutput,
    output_key="final_output"
)