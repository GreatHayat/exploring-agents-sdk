import asyncio
from agents import Agent, Runner
from tools.weather import get_current_weather

# Set up the agent
weather_agent = Agent(
    name="Weather Agent",
    instructions="Get the current weather for a given location.",
    model="gpt-4o-mini",
    tools=[get_current_weather]
)

async def main():
    messages = []
    while True:
        question = input("Please enter your question: ")
        messages.append({"role": "user", "content": question})
        response = await Runner.run(weather_agent, messages)
        print(f"AI Assistant's response: {response.final_output}")

        messages.append({"role": "assistant", "content": response.final_output})
        # print(response.to_input_list())


if __name__ == "__main__":
    asyncio.run(main())