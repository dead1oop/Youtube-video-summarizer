"""Initialize Streamlit session state defaults."""

import streamlit as st


def init_session_state() -> None:
    defaults = {
        "transcript_data": None,
        "current_url": "",
        "chat_messages": [],
        "chatbot": None,
        "summary": None,
        "notes": None,
        "mcqs": None,
        "sentiment": None,
        "keywords": None,
        "interview_questions": None,
        "summary_error": None,
        "summary_style": "concise",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
