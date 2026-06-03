import streamlit as st

from modules.interview_questions import InterviewQuestionGenerator


def render() -> None:
    data = st.session_state["transcript_data"]
    st.header("🎯 Interview Prep")

    count = st.slider("Number of questions", 5, 20, 10)

    if st.button("Generate Interview Questions", type="primary"):
        with st.spinner("Generating..."):
            st.session_state["interview_questions"] = (
                InterviewQuestionGenerator().generate(data["transcript"], count)
            )

    if st.session_state.get("interview_questions"):
        st.markdown(st.session_state["interview_questions"])
