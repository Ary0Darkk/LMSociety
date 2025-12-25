import dspy
import agents.models as llms


class Philosopher(dspy.Signature):
    """Think deeply about the moral and ethical implications of a project."""

    proposal = dspy.InputField(desc="The initial idea for a societal project")
    ethics_framework = dspy.OutputField(
        desc="Moral principles and potential ethical risks"
    )


class Engineer(dspy.Signature):
    """Translate ethical frameworks into technical specifications and blueprints."""

    ethics_framework = dspy.InputField(
        desc="The constraints provided by the philosopher"
    )
    technical_plan = dspy.OutputField(
        desc="A detailed build-plan with materials and logic"
    )


class Government(dspy.Signature):
    """Review technical plans and approve or provide regulatory feedback."""

    technical_plan = dspy.InputField()
    verdict = dspy.OutputField(desc="Approved, Rejected, or Needs Revision")
    reasoning = dspy.OutputField(desc="Legal and safety justification for the verdict")


class SocietyOfThree(dspy.Module):
    def __init__(self):
        super().__init__()
        # We use ChainOfThought so they "think" before they speak
        self.thinker = dspy.ChainOfThought(Philosopher)
        self.builder = dspy.ChainOfThought(Engineer)
        self.regulator = dspy.ChainOfThought(Government)

    def forward(self, proposal):
        # 1. Philosopher defines the ethics
        moral_brief = self.thinker(proposal=proposal)

        # 2. Engineer uses those ethics to design the plan
        blueprint = self.builder(ethics_framework=moral_brief.ethics_framework)

        # 3. Government regulates the blueprint
        final_decision = self.regulator(technical_plan=blueprint.technical_plan)

        return dspy.Prediction(
            ethics=moral_brief.ethics_framework,
            plan=blueprint.technical_plan,
            verdict=final_decision.verdict,
            reasoning=final_decision.reasoning,
        )


# Initialize your society
society = SocietyOfThree()

# Run it with a specific model context
with dspy.context(lm=llms.deepseek_lm):
    result = society(proposal="Building a city where AI controls the traffic lights.")

print(f"GOVERNMENT VERDICT: {result.verdict}")
print(f"REASONING: {result.reasoning}")
