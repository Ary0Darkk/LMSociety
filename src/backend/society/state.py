from typing import Optional


class AgentState:
    def __init__(self, name: str, persona: str):
        self.name = name
        self.persona = persona
        self.internal_monologue: Optional[str] = None
        self.verbal_response: Optional[str] = None

    def set_response(self, internal_monologue: str, verbal_response: str):
        self.internal_monologue = internal_monologue
        self.verbal_response = verbal_response

    def get_public_context(self) -> str:
        return self.verbal_response or ""

    def get_internal_context(self) -> str:
        return self.internal_monologue or ""
