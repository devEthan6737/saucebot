from langchain.agents.middleware import wrap_model_call
from langchain_core.messages import AIMessage, HumanMessage

# how many chat messages (the user's and the bot's answers) the model gets to see
# the tool calls and their results in between don't count, they are all kept
REMEMBERED_MESSAGES = 10

def _is_chat (message):
    return isinstance(message, HumanMessage) or (isinstance(message, AIMessage) and not message.tool_calls)

# the model only receives the last messages, not the whole conversation
# it always starts on a user message, so a tool result never loses its tool call
@wrap_model_call
async def memory (request, handler):
    messages = request.messages
    chat = [ i for i, m in enumerate(messages) if _is_chat(m) ]

    if len(chat) > REMEMBERED_MESSAGES:
        start = chat[-REMEMBERED_MESSAGES]
        while not isinstance(messages[start], HumanMessage):
            start += 1
        request = request.override(messages=messages[start:])

    return await handler(request)
