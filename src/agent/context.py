from dataclasses import dataclass

# data passed to the agent on every call, tools read it from runtime.context
@dataclass
class Context:
    userId: int
