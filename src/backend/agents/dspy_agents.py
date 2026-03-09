import dspy


class DebateSignature(dspy.Signature):
    topic = dspy.InputField()
    persona = dspy.InputField()
    context = dspy.InputField()

    response = dspy.OutputField()


class DebateAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.Predict(DebateSignature)

    def forward(self, topic, persona, context):
        return self.generate(topic=topic, persona=persona, context=context)
