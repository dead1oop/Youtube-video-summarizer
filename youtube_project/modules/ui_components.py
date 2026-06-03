"""Reusable Streamlit UI components."""

import streamlit as st

from utils.history import VideoHistory

PAGES = [
    "Dashboard",
    "📄 Transcript",
    "📝 Summary",
    "📚 Study Notes",
    "❓ MCQ Quiz",
    "💬 Chat with Video",
    "📊 Sentiment",
    "🔑 Keywords",
    "🎯 Interview Prep",
]


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## 🎓 SmartTube AI")
        st.caption("YouTube Video Summarizer & Study Assistant")
        st.markdown("---")

        selected = st.radio("Navigation", PAGES, label_visibility="collapsed")

        st.markdown("---")
        if st.session_state.get("transcript_data"):
            data = st.session_state["transcript_data"]
            st.image(data.get("thumbnail", ""), use_container_width=True)
            st.markdown(f"**{data.get('title', 'Unknown')}**")
            st.caption(f"{data.get('word_count', 0)} words")

        st.markdown("---")
        if st.button("🗑️ Clear Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    return selected


def render_header() -> None:
    st.markdown(
        """
        <div style="text-align:center; padding: 0.5rem 0 1rem;">
            <h1 style="margin:0;">🎓 SmartTube AI</h1>
            <p style="color:#888; margin:0.25rem 0 0;">YouTube Video Summarizer & Study Assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    history = VideoHistory()
    count = len(history.get_all())
    st.markdown("---")
    st.caption(f"SmartTube AI · {count} videos in history · Set GEMINI_API_KEY for AI features")
