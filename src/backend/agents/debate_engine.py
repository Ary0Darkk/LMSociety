from backend.agents.dspy_agents import DebateAgent
from backend.vector_store.chroma_store import retrieve_context, store_message

agent_model = DebateAgent()


def generate_agent_response(agent, topic, context):
    context = retrieve_context(topic)
    result = agent_model(topic=topic, persona=agent["persona"], context=context)

    message = result.response

    store_message(agent["name"], message)

    return message


# if __name__ == "__main__":
# philosopher_agent = {
#     "name": "Philosopher",
#     "persona": "A deep thinker focused on ethics, history, and social dynamics.",
# }
# debate_topic = "Why is the population in India so high?"
# current_context = (
#     "Historical lack of access to family planning and social-economic factors."
# )

# Call the function with the dictionary
# message = generate_agent_response(
# agent=philosopher_agent, topic=debate_topic, context=current_context
# )

# print(f"--- {philosopher_agent['name']}'s Response ---")
# print(message)
