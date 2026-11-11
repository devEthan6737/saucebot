from datetime import date
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt
from langgraph.checkpoint.memory import InMemorySaver

from src.agent.model import model
from src.chef.context import ChefContext
from src.chef.tools import tools

personality = (Path(__file__).parent / "personality.txt").read_text().strip()

def _ingredients (ingredients):
    return "\n".join(f"- {i['name']}: {i['quantity']:g} {i['unit']}" for i in ingredients) or "- none"

# the recipe of the session goes in the prompt
@dynamic_prompt
def prompt (request):
    recipe = request.runtime.context.recipe
    return (
        f"{personality}\n\n"
        f"Recipe: {recipe['name']} ({recipe.get('description', '')}), for {recipe.get('servings', 1)} servings.\n"
        f"Ingredients the user has:\n{_ingredients(recipe.get('in_stock', []))}\n"
        f"Ingredients the user is missing:\n{_ingredients(recipe.get('missing', []))}\n"
        f"Today is {date.today().isoformat()}."
    )

# no memory trimming here: the chef reads the whole session, which is deleted when it ends
checkpointer = InMemorySaver()

agent = create_agent(
    model,
    tools,
    middleware=[ prompt ],
    context_schema=ChefContext,
    checkpointer=checkpointer,
)

# the chef answer comes in pieces, so it can start talking before it has finished writing
async def talk (token: str, userId: int, recipe: dict, text: str):
    stream = agent.astream(
        { "messages": [{ "role": "user", "content": text }] },
        config={ "configurable": { "thread_id": token } },
        context=ChefContext(token=token, userId=userId, recipe=recipe),
        stream_mode="messages",
    )

    async for chunk, metadata in stream:
        if metadata.get("langgraph_node") == "model" and isinstance(chunk.content, str) and chunk.content:
            yield chunk.content

# forgets the whole conversation of a session
def forget (token: str):
    checkpointer.delete_thread(token)
