import streamlit as st

from modules.summarizer import Summarizer


def render() -> None:
    data = st.session_state.get("transcript_data")
    if not data or not data.get("transcript"):
        st.warning("No transcript loaded. Analyze a video first.")
        return

    st.header("📝 Summary")
    transcript = data["transcript"]
    st.caption(f"Transcript: {data.get('word_count', 0)} words")

    style = st.selectbox("Summary style", ["concise", "detailed", "eli5"])

    col1, col2 = st.columns(2)
    with col1:
        generate_btn = st.button("Generate Summary", type="primary", use_container_width=True)
    with col2:
        auto = st.checkbox("Auto-generate on page load", value=True)

    if generate_btn or (auto and not st.session_state.get("summary")):
        with st.spinner("Generating summary..."):
            try:
                summary = Summarizer().summarize(transcript, style)
                st.session_state["summary"] = summary
                st.session_state["summary_style"] = style
                st.session_state["summary_error"] = None
            except Exception as exc:
                st.session_state["summary"] = None
                st.session_state["summary_error"] = str(exc)

    if st.session_state.get("summary_error"):
        st.error(f"Summary failed: {st.session_state['summary_error']}")

    summary = st.session_state.get("summary")
    if summary:
        st.markdown(summary)
        st.download_button(
            "Download Summary",
            summary,
            file_name=f"{data.get('video_id', 'video')}_summary.md",
        )
    elif not generate_btn:
        st.info("Click **Generate Summary** or enable auto-generate above.")
