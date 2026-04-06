from datetime import datetime

from backend.agents.dspy_agents import DebateAgent
from backend.vector_store.chroma_store import retrieve_context, store_message
from backend.society import filter_by_trust

agent_model = DebateAgent()


def truncate_words(text: str, max_words: int) -> str:
    """Truncate text to max words."""
    if not text:
        return ""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."


def generate_agent_response(
    agent, topic, history: list = None, user_prompt=None, target_agent=None
):
    """
    Generate the agent response given topic and context
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context = retrieve_context(topic)
    context = f"{context}\n\nCurrent timestamp: {timestamp}"

    # Add previous messages to context so agents can respond to each other
    if history:
        context += "\n\nPrevious statements in this debate:\n"
        for msg in history[-6:]:  # Last 6 messages to keep context but not overload
            context += f"- {msg['agent']}: {msg['content']}\n"

    if user_prompt:
        context = f"{context}\n\nUser prompt to {agent['name']}: {user_prompt}"

    prompt = f"""Persona: {agent["persona"]}
Topic: {topic}
Context: {context}

You are in a debate. Listen to what others said, then respond to them specifically.
IMPORTANT: Reference or react to what others said. Don't just state your view.

verbal_response: (1-2 sentences, reference what someone said)
internal_monologue: (1 quick thought, your private reaction)
withheld_info: (1 thing you don't say)
subtext: (1 hint)

Keep each under 20 words."""

    result = agent_model(topic=topic, persona=agent["persona"], context=prompt)

    internal_monologue = result.internal_monologue
    verbal_response = result.verbal_response
    withheld_info = result.withheld_info or ""
    subtext = result.subtext or ""

    # Enforce word limits
    verbal_response = truncate_words(verbal_response, 30)
    internal_monologue = truncate_words(internal_monologue, 15)
    withheld_info = truncate_words(withheld_info, 15)
    subtext = truncate_words(subtext, 15)

    leaked_info = ""
    if target_agent and internal_monologue:
        leaked_info = filter_by_trust(internal_monologue, target_agent, agent["name"])
        if leaked_info:
            context = f"{context}\n\n[Private thoughts revealed from {agent['name']}: {leaked_info}]"

    store_message(agent["name"], verbal_response)

    return {
        "verbal_response": verbal_response,
        "internal_monologue": internal_monologue,
        "withheld_info": withheld_info,
        "subtext": subtext,
        "leaked_to": target_agent if leaked_info else None,
    }


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
