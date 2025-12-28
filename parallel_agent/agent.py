from dotenv import load_dotenv
load_dotenv()
from google.adk.agents import Agent, ParallelAgent
from google.adk.models.lite_llm import LiteLlm

llm = LiteLlm(model="openai/gpt-4o", temperature=0.5)

import os
os.environ["OTEL_PYTHON_DISABLED"] = "true" # OpenTelemetry issues -> regarding internal asyncio package which beaks the 'adk web'


# Hotel Search Agent - Finds accommodation options
hotel_search_agent = Agent(
    name="HotelSearchAgent",
    model=llm,
    # tools=[google_search],
    description="An agent that searches for hotels and accommodation options in a given destination",
    instruction="""
    You are a hotel booking specialist. You will be given a destination, and you will search for:
    - Popular hotels in the area
    - Different price ranges (budget, mid-range, luxury)
    - Hotel amenities and ratings
    - Location advantages
    Provide a summary of the best accommodation options with brief descriptions.
    ONLY research for hotels and nothing else.
    """,
    output_key="hotel_options",
)

# Restaurant Search Agent - Finds dining options
restaurant_search_agent = Agent(
    name="RestaurantSearchAgent",
    model=llm,
    # tools=[google_search],
    description="An agent that searches for restaurants and dining experiences in a given destination",
    instruction="""
    You are a food and dining expert. You will be given a destination and you will search for:
    - Top-rated restaurants and cafes
    - Local cuisine specialties
    - Different dining price ranges
    - Unique dining experiences
    Provide a summary of the best dining options with cuisine types and highlights.
    Only research for restaurants and nothing else.
    """,
    output_key="restaurant_options",
)

# Activities Search Agent - Finds things to do
activities_search_agent = Agent(
    name="ActivitiesSearchAgent",
    model=llm,
    # tools=[google_search],
    description="An agent that searches for activities and attractions in a given destination",
    instruction="""
    You are a local activities expert. You will be given a destination and you will search for:
    - Popular tourist attractions
    - Outdoor activities and adventures
    - Cultural experiences and museums
    - Entertainment and nightlife options
    Provide a summary of the best activities with brief descriptions and recommendations.
    Only research for activities and nothing else.
    """,
    output_key="activity_options",
)

summrise_agent = Agent(
    name="SummarizeAgent",
    model=llm,
    description="An agent that summarizes the findings from hotel, restaurant, and activities search agents",
    instruction="""
    You are a travel planner. Using the outputs from the 'hotel_options', 'restaurant_options', and 'activity_options', create a comprehensive summary for a trip plan that includes:
    - Top hotel options with brief descriptions
    - Recommended restaurants with cuisine types
    - Suggested activities and attractions
    Format the final output as a clear and concise travel plan.
    """,
)

# Main parallel agent that runs all search agents simultaneously
root_agent = ParallelAgent(
    name="TravelPlanningSystem",
    description="A comprehensive system that simultaneously searches for hotels, restaurants, and activities for trip planning",
    sub_agents=[hotel_search_agent, restaurant_search_agent, activities_search_agent],
)