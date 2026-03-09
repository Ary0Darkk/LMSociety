import streamlit as st
import requests
import time

API = "http://localhost:8000"

st.title("Society Debate")

debate_id = st.number_input("Debate ID", step=1)

if "agents" not in st.session_state:
    st.session_state.agents = []

if "messages" not in st.session_state:
    st.session_state.messages = {}

if st.button("Load Debate"):
    r = requests.get(f"{API}/debate/{debate_id}/agents")

    agents = r.json()

    st.session_state.agents = agents

    for agent in agents:
        st.session_state.messages[agent["name"]] = []

# -----------------------------
# AGENT COLUMNS
# -----------------------------

agents = st.session_state.agents

if agents:
    cols = st.columns(len(agents))

    for i, agent in enumerate(agents):
        with cols[i]:
            st.subheader(agent["name"])

            status_placeholder = st.empty()

            message_placeholder = st.empty()

            messages = st.session_state.messages[agent["name"]]

            text = "\n\n".join(messages)

            message_placeholder.text_area("Messages", text, height=300)

# -----------------------------
# RUN ROUND
# -----------------------------

if st.button("Run Debate Round"):
    agents = st.session_state.agents

    for agent in agents:
        with st.spinner(f"{agent['name']} thinking..."):
            response = requests.post(
                f"{API}/debate/{debate_id}/speak", json={"agent": agent["name"]}
            )

            msg = response.json()["message"]

            st.session_state.messages[agent["name"]].append(msg)

            time.sleep(1)

    st.rerun()
