import streamlit as st

from utils.history import VideoHistory


def render() -> None:
    st.header("📊 Dashboard")
    history = VideoHistory()
    items = history.get_all()

    if not items:
        st.info("No videos analyzed yet. Enter a YouTube URL above to begin.")
        return

    cols = st.columns(3)
    st.metric("Videos Analyzed", len(items))
    if st.session_state.get("transcript_data"):
        data = st.session_state["transcript_data"]
        cols[1].metric("Current Words", data.get("word_count", 0))
        cols[2].metric("Language", data.get("language", "en"))

    st.subheader("Recent Videos")
    for item in items[:10]:
        col_img, col_info = st.columns([1, 4])
        with col_img:
            if item.get("thumbnail"):
                st.image(item["thumbnail"], width=120)
        with col_info:
            st.markdown(f"**{item.get('title', 'Unknown')}**")
            st.caption(item.get("url", ""))
            st.caption(f"Analyzed: {item.get('analyzed_at', '')[:16]}")
        st.divider()

    if st.button("Clear History"):
        history.clear()
        st.rerun()
