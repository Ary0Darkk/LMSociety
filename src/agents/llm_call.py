import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()


def run_gemini_model(prompt: str) -> str:
    gemini_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    gemini_result = gemini_model.invoke(prompt)

    return gemini_result


def run_minmax_model(prompt: str):
    llm = HuggingFaceEndpoint(repo_id="MiniMaxAI/MiniMax-M2", task="text-generation")

    model = ChatHuggingFace(llm=llm)

    result = model.invoke(prompt)

    return result


def run_gptoss_model(prompt: str):
    llm = ChatOpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv("HF_TOKEN"),
        model="openai/gpt-oss-20b:fireworks-ai",
        temperature=0.7,
    )

    result = llm.invoke(prompt)
    return result


def run_deepseek_model(prompt: str):
    llm = ChatOpenAI(
        base_url="https://router.huggingface.co/v1",  # Standard HF Inference endpoint
        api_key=os.getenv("HF_TOKEN"),
        model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",  # Example DeepSeek model
        temperature=0.7,
    )

    result = llm.invoke(prompt)
    return result
