from typing import Dict

# NOTE : Add more realistic trust system
# Hardcoded -Trust system
TRUST_MATRIX: Dict[str, Dict[str, float]] = {
    "Philosopher": {
        "Engineer": 0.8,
        "Government": 0.5,
        "Citizen": 0.3,
    },
    "Engineer": {
        "Philosopher": 0.7,
        "Government": 0.6,
        "Citizen": 0.4,
    },
    "Government": {
        "Philosopher": 0.6,
        "Engineer": 0.7,
        "Citizen": 0.2,
    },
    "Citizen": {
        "Philosopher": 0.5,
        "Engineer": 0.6,
        "Government": 0.3,
    },
}


def filter_by_trust(
    internal_monologue: str, target_agent: str, source_agent: str
) -> str:
    """Logic for  trust between agents"""
    trust_level = TRUST_MATRIX.get(source_agent, {}).get(target_agent, 0.5)

    if trust_level >= 0.7:
        return internal_monologue
    elif trust_level >= 0.4:
        sentences = internal_monologue.split(". ")
        reveal_count = int(len(sentences) * trust_level)
        return ". ".join(sentences[:reveal_count]) + "."
    else:
        return ""
