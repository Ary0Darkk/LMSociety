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

if "internal_monologues" not in st.session_state:
    st.session_state.internal_monologues = {}

if "withheld_info" not in st.session_state:
    st.session_state.withheld_info = {}

if "subtexts" not in st.session_state:
    st.session_state.subtexts = {}

if st.button("Load Debate"):
    r = requests.get(f"{API}/debate/{debate_id}/agents")

    agents = r.json()

    st.session_state.agents = agents

    for agent in agents:
        st.session_state.messages[agent["name"]] = []
        st.session_state.internal_monologues[agent["name"]] = []
        st.session_state.withheld_info[agent["name"]] = []
        st.session_state.subtexts[agent["name"]] = []

    r = requests.get(f"{API}/debate/{debate_id}")
    if r.status_code == 200:
        msgs = r.json()
        for msg in msgs:
            agent_name = msg.get("agent_name", "")
            for key in st.session_state.messages:
                if key in agent_name:
                    st.session_state.messages[key].append(msg.get("content", ""))
                    st.session_state.internal_monologues[key].append(
                        msg.get("internal_monologue") or ""
                    )
                    st.session_state.withheld_info[key].append(
                        msg.get("withheld_info") or ""
                    )
                    st.session_state.subtexts[key].append(msg.get("subtext") or "")
                    break

# -----------------------------
# AGENT COLUMNS
# -----------------------------

agents = st.session_state.agents

if agents:
    cols = st.columns(len(agents))

    for i, agent in enumerate(agents):
        with cols[i]:
            st.subheader(agent["name"])

            message_placeholder = st.empty()
            messages = st.session_state.messages[agent["name"]]
            text = "\n\n".join(messages)
            message_placeholder.text_area("Verbal Response", text, height=150)

            internal_placeholder = st.empty()
            internal_msgs = st.session_state.internal_monologues[agent["name"]]
            internal_text = "\n\n".join([m for m in internal_msgs if m])
            internal_placeholder.text_area(
                "Internal Monologue", internal_text, height=100
            )

            withheld_placeholder = st.empty()
            withheld_msgs = st.session_state.withheld_info[agent["name"]]
            withheld_text = "\n\n".join([m for m in withheld_msgs if m])
            withheld_placeholder.text_area("Withheld Info", withheld_text, height=80)

            subtext_placeholder = st.empty()
            subtext_msgs = st.session_state.subtexts[agent["name"]]
            subtext_text = "\n\n".join([m for m in subtext_msgs if m])
            subtext_placeholder.text_area("Subtext", subtext_text, height=80)

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

            result = response.json()
            msg = result.get("message", "")

            st.session_state.messages[agent["name"]].append(msg)

            internal_monologue = result.get("internal_monologue", "")
            if internal_monologue:
                st.session_state.internal_monologues[agent["name"]].append(
                    internal_monologue
                )

            withheld = result.get("withheld_info", "")
            if withheld:
                st.session_state.withheld_info[agent["name"]].append(withheld)

            subtext = result.get("subtext", "")
            if subtext:
                st.session_state.subtexts[agent["name"]].append(subtext)

            time.sleep(1)

    st.rerun()
