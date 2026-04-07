import streamlit as st
import requests

st.title("Setup Society")

num_agents = st.slider("Number of agents", 2, 6, 3)

topic = st.text_input("Discussion topic")

model = st.selectbox("Select LLM Model", ["Gemini", "MiniMax", "GPT-OSS", "DeepSeek"])

agents = []

for i in range(num_agents):
    name = st.text_input(f"Agent {i + 1} name", key=f"name{i}")

    persona = st.text_area(f"Agent {i + 1} persona", key=f"persona{i}")

    agents.append({"name": name, "persona": persona})

if st.button("Start Debate"):
    r = requests.post(
        "http://localhost:8000/debate/start",
        json={"topic": topic, "agents": agents, "model": model},
    )

    st.write(r.json())
