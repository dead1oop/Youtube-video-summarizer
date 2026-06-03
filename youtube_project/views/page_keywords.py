import streamlit as st

from modules.keywords import KeywordExtractor


def render() -> None:
    data = st.session_state["transcript_data"]
    st.header("🔑 Keywords")

    top_n = st.slider("Number of keywords", 5, 25, 15)

    if st.button("Extract Keywords", type="primary"):
        with st.spinner("Extracting..."):
            st.session_state["keywords"] = KeywordExtractor().extract(
                data["transcript"], top_n
            )

    keywords = st.session_state.get("keywords")
    if not keywords:
        return

    for item in keywords:
        st.progress(min(item["score"] / max(k["score"] for k in keywords), 1.0))
        st.markdown(f"**{item['keyword']}** — score: {item['score']}")
