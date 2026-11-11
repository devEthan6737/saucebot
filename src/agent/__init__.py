from datetime import date
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt
from langgraph.checkpoint.memory import InMemorySaver

from src.agent.model import model
from src.agent.context import Context
from src.agent.tools import tools

personality = (Path(__file__).parent / "personality.txt").read_text().strip()

# built on every call so the agent always knows today's date
@dynamic_prompt
def prompt (request):
    return f"{personality}\nToday is {date.today().isoformat()}."

agent = create_agent(
    model,
    tools,
    middleware=[ prompt ],
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

# each user has its own conversation thread
async def ask (userId: int, text: str) -> str:
    result = await agent.ainvoke(
        { "messages": [{ "role": "user", "content": text }] },
        config={ "configurable": { "thread_id": str(userId) } },
        context=Context(userId=userId),
    )
    return result["messages"][-1].content
