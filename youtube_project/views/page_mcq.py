import streamlit as st

from modules.mcq_generator import MCQGenerator


def render() -> None:
    data = st.session_state["transcript_data"]
    st.header("❓ MCQ Quiz")

    count = st.slider("Number of questions", 3, 10, 5)

    if st.button("Generate Quiz", type="primary"):
        with st.spinner("Generating questions..."):
            st.session_state["mcqs"] = MCQGenerator().generate(data["transcript"], count)

    mcqs = st.session_state.get("mcqs")
    if not mcqs:
        return

    for i, q in enumerate(mcqs):
        st.markdown(f"**Q{i + 1}.** {q.get('question', '')}")
        options = q.get("options", [])
        answer = st.radio(
            f"Choose answer for Q{i + 1}",
            options,
            key=f"mcq_{i}",
            index=None,
        )
        if answer is not None:
            correct = options[q.get("answer", 0)] if options else None
            if answer == correct:
                st.success("Correct!")
            else:
                st.error(f"Incorrect. Correct answer: {correct}")
        st.divider()
