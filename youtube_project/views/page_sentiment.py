import streamlit as st

from modules.sentiment import SentimentAnalyzer


def render() -> None:
    data = st.session_state["transcript_data"]
    st.header("📊 Sentiment Analysis")

    if st.button("Analyze Sentiment", type="primary"):
        with st.spinner("Analyzing..."):
            st.session_state["sentiment"] = SentimentAnalyzer().analyze(
                data["transcript"]
            )

    result = st.session_state.get("sentiment")
    if not result:
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Overall", result["label"])
    c2.metric("Polarity", result["polarity"])
    c3.metric("Subjectivity", result["subjectivity"])

    if result.get("highlights"):
        st.subheader("Notable passages")
        for h in result["highlights"]:
            st.markdown(f"- ({h['polarity']:+.2f}) {h['text']}")
