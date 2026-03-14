import dspy
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini
gemini_lm = dspy.LM(
    "gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    num_retries=3,
)

# MiniMax
minimax_lm = dspy.LM(
    "openai/MiniMaxAI/MiniMax-M2",
    api_base="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
    num_retries=3,
)

# GPT-OSS
gptoss_lm = dspy.LM(
    "openai/openai/gpt-oss-20b:fireworks-ai",
    api_base="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
    temperature=0.7,
    num_retries=3,
)

# DeepSeek
deepseek_lm = dspy.LM(
    "openai/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    api_base="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
    temperature=0.7,
    num_retries=3,
)

LLM_REGISTRY = {
    "Gemini": gemini_lm,
    "MiniMax": minimax_lm,
    "GPT-OSS": gptoss_lm,
    "DeepSeek": deepseek_lm,
}


# choose default model
# dspy.settings.configure(lm=deepseek_lm)


# example
# dspy.settings.configure(lm=LLM_REGISTRY["Gemini"])
# predict = dspy.Predict("question -> answer")

# prediction = predict(question="What is the capital of India?")

# print(prediction.answer)
