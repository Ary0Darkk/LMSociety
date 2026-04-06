import dspy


class DebateSignature(dspy.Signature):
    """Generate brief dialogue output."""

    topic = dspy.InputField()
    persona = dspy.InputField()
    context = dspy.InputField()

    internal_monologue = dspy.OutputField()
    verbal_response = dspy.OutputField()
    withheld_info = dspy.OutputField()
    subtext = dspy.OutputField()


class DebateAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.Predict(DebateSignature)

    def forward(self, topic, persona, context):
        prompt = f"""You are {persona}. On topic: {topic}.
Previous: {context}

Write very briefly for each:

verbal_response: A short reply.
internal_monologue: One quick thought.
withheld_info: One thing you hide.
subtext: One hint."""

        return self.generate(topic=topic, persona=persona, context=prompt)
