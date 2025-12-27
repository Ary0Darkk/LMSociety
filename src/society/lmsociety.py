import dspy
import agents.models as llm


# signatures
class Philosopher(dspy.Signature):
    """Think deeply about the moral implications of a project."""

    proposal = dspy.InputField()
    ethics_framework = dspy.OutputField()


class Engineer(dspy.Signature):
    """Translate ethical frameworks into technical plans."""

    ethics_framework = dspy.InputField()
    technical_plan = dspy.OutputField()


class Government(dspy.Signature):
    """Review plans and provide regulatory feedback."""

    technical_plan = dspy.InputField()
    verdict = dspy.OutputField()
    reasoning = dspy.OutputField()


class Citizen(dspy.Signature):
    """Provide a final human-centric review on how this affects daily life."""

    proposal = dspy.InputField()
    verdict = dspy.InputField()
    feedback = dspy.OutputField(desc="Emotional and practical reaction from the public")


# society Module
class SocietyOfFour(dspy.Module):
    def __init__(self, models):
        super().__init__()
        self.models = models  # Dictionary of your 4 different LLM objects

        # Define the reasoning style for each
        self.thinker = dspy.ChainOfThought(Philosopher)
        self.builder = dspy.ChainOfThought(Engineer)
        self.regulator = dspy.ChainOfThought(Government)
        self.public = dspy.ChainOfThought(Citizen)

    def forward(self, proposal):
        # We wrap each call in a specific context to force a different model

        with dspy.context(lm=self.models["philosopher"]):
            moral_brief = self.thinker(proposal=proposal)

        with dspy.context(lm=self.models["engineer"]):
            blueprint = self.builder(ethics_framework=moral_brief.ethics_framework)

        with dspy.context(lm=self.models["government"]):
            gov_review = self.regulator(technical_plan=blueprint.technical_plan)

        with dspy.context(lm=self.models["citizen"]):
            reaction = self.public(proposal=proposal, verdict=gov_review.verdict)

        return dspy.Prediction(
            ethics=moral_brief.ethics_framework,
            plan=blueprint.technical_plan,
            verdict=gov_review.verdict,
            citizen_reaction=reaction.feedback,
        )


# assign different models
agent_models = {
    "philosopher": llm.deepseek_lm,  # Wise and slow
    "engineer": llm.gemini_lm,  # Good at technical logic
    "government": llm.gptoss_lm,  # Large context for regulations
    "citizen": llm.minimax_lm,  # Fast, "everyman" model
}

society = SocietyOfFour(agent_models)
result = society(proposal="AI-controlled city traffic lights")

print(f"Citizen Feedback: {result.citizen_reaction}")
