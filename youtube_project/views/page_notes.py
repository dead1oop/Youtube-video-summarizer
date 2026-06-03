import streamlit as st

from modules.notes_generator import NotesGenerator


def render() -> None:
    data = st.session_state["transcript_data"]
    st.header("📚 Study Notes")

    if st.button("Generate Study Notes", type="primary"):
        with st.spinner("Generating notes..."):
            st.session_state["notes"] = NotesGenerator().generate(data["transcript"])

    if st.session_state.get("notes"):
        st.markdown(st.session_state["notes"])
        st.download_button(
            "Download Notes",
            st.session_state["notes"],
            file_name=f"{data.get('video_id', 'notes')}_notes.md",
        )
