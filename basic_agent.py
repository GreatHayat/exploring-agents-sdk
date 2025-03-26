import asyncio
from agents import Agent, Runner

agent = Agent(
    name="AI Assistant",
    instructions="You are a helpful AI assistant to answer user queries.",
    model="gpt-4o-mini"
)

async def main():
    messages = []
    while True:
        question = input("Please enter your question: ")
        messages.append({"role": "user", "content": question})
        response = await Runner.run(agent, messages)
        print(f"AI Assistant's response: {response.final_output}")

        messages.append({"role": "assistant", "content": response.final_output})
        # print(response.to_input_list())


if __name__ == "__main__":
    asyncio.run(main())