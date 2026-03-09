from backend.agents.dspy_agents import DebateAgent
from backend.vector_store.chroma_store import retrieve_context
from backend.vector_store.chroma_store import store_message

agent_model = DebateAgent()


def generate_agent_response(agent, topic):
    context = retrieve_context(topic)

    result = agent_model(topic=topic, persona=agent["persona"], context=context)

    message = result.response

    store_message(agent["name"], message)

    return message
