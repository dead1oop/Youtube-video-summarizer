"""
SmartTube AI – YouTube Video Summarizer & Study Assistant
Main Streamlit Application Entry Point
"""

# SSL fix MUST run before any network library imports
import os
import ssl
import sys

os.environ["DISABLE_SSL_VERIFY"] = "1"
os.environ["PYTHONHTTPSVERIFY"] = "0"
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except Exception:
    pass

_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ROOT)

from modules.env_loader import load_env
from modules.ssl_fix import apply_ssl_fix

load_env()
apply_ssl_fix()

import streamlit as st
from modules.settings import inject_premium_theme
from modules.ui_components import render_sidebar, render_header, render_footer
from modules.transcript import TranscriptExtractor
from modules.summarizer import Summarizer

from utils.session_state import init_session_state
from utils.history import VideoHistory
from views import (
    page_transcript,
    page_summary,
    page_notes,
    page_mcq,
    page_chat,
    page_sentiment,
    page_keywords,
    page_interview,
    page_dashboard,
)

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartTube AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Load CSS ─────────────────────────────────────────────────────────────────
# ─── Main App ─────────────────────────────────────────────────────────────────
def main() -> None:
    """Main application function."""
    inject_premium_theme()
    init_session_state()

    # Sidebar navigation
    selected_page = render_sidebar()

    # Header
    render_header()

    # URL Input section (always visible)
    render_url_input()

    # Route to selected page (custom sidebar nav — not Streamlit pages/ folder)
    st.markdown("---")
    if st.session_state.get("transcript_data"):
        route_page(selected_page)
    elif selected_page == "Dashboard":
        page_dashboard.render()
    else:
        st.info("👆 Enter a YouTube URL above and click **Analyze Video** to get started!")

    render_footer()


def render_url_input() -> None:
    """Render the YouTube URL input section."""
    st.markdown("---")
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        url = st.text_input(
            "🔗 YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            key="youtube_url_input",
            help="Paste any YouTube video URL to begin analysis",
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        language = st.selectbox(
            "Language",
            ["en", "hi", "es", "fr", "de", "ja", "ko", "pt", "zh"],
            key="transcript_language",
        )

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 Analyze Video", type="primary", use_container_width=True)

    if analyze_btn and url:
        process_video(url, language)
    elif analyze_btn and not url:
        st.warning("Please enter a YouTube URL first.")


def process_video(url: str, language: str = "en") -> None:
    """
    Extract transcript and initialize all modules for the given URL.

    Args:
        url: YouTube video URL
        language: Transcript language code
    """
    with st.spinner("🔍 Extracting transcript..."):
        extractor = TranscriptExtractor()
        result = extractor.extract(url, language)

        if result["success"]:
            st.session_state["transcript_data"] = result
            st.session_state["current_url"] = url
            st.session_state["chat_messages"] = []
            st.session_state["chatbot"] = None
            for key in ("summary", "notes", "mcqs", "sentiment", "keywords", "interview_questions", "summary_error"):
                st.session_state[key] = None

            with st.spinner("📝 Generating summary..."):
                try:
                    st.session_state["summary"] = Summarizer().summarize(
                        result["transcript"], "concise"
                    )
                    st.session_state["summary_error"] = None
                except Exception as exc:
                    st.session_state["summary"] = None
                    st.session_state["summary_error"] = str(exc)

            history = VideoHistory()
            history.add(url, result.get("title", "Unknown"), result.get("thumbnail", ""))

            method = result.get("fetch_method", "")
            st.success(
                f"✅ Transcript extracted! ({result['word_count']} words)"
                + (f" via {method}" if method else "")
            )
            if st.session_state.get("summary"):
                st.success("✅ Summary generated! Open **📝 Summary** in the sidebar.")
            elif st.session_state.get("summary_error"):
                st.warning(f"Summary could not be generated: {st.session_state['summary_error']}")
            st.rerun()
        else:
            st.error(f"❌ {result['error']}")


def route_page(page: str) -> None:
    """
    Route to the appropriate page module.

    Args:
        page: Page name string
    """
    page_map = {
        "Dashboard": page_dashboard.render,
        "📄 Transcript": page_transcript.render,
        "📝 Summary": page_summary.render,
        "📚 Study Notes": page_notes.render,
        "❓ MCQ Quiz": page_mcq.render,
        "💬 Chat with Video": page_chat.render,
        "📊 Sentiment": page_sentiment.render,
        "🔑 Keywords": page_keywords.render,
        "🎯 Interview Prep": page_interview.render,
    }

    render_func = page_map.get(page, page_dashboard.render)
    render_func()


if __name__ == "__main__":
    main()