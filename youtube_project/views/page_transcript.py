import streamlit as st


def render() -> None:
    data = st.session_state["transcript_data"]
    st.header("📄 Transcript")
    st.markdown(f"**{data.get('title', 'Unknown')}**")
    st.caption(f"{data.get('word_count', 0)} words · Language: {data.get('language', 'en')}")

    search = st.text_input("Search in transcript", "")
    text = data.get("transcript", "")
    if search:
        lines = [ln for ln in text.split(". ") if search.lower() in ln.lower()]
        text = ". ".join(lines) if lines else "No matches found."

    st.text_area("Full Transcript", text, height=400)
    st.download_button(
        "Download Transcript",
        data.get("transcript", ""),
        file_name=f"{data.get('video_id', 'transcript')}.txt",
    )
