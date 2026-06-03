import streamlit as st

from modules.chatbot import VideoChatbot


def render() -> None:
    data = st.session_state["transcript_data"]
    st.header("💬 Chat with Video")

    if st.session_state.get("chatbot") is None:
        st.session_state["chatbot"] = VideoChatbot(
            data["transcript"], data.get("title", "")
        )

    for msg in st.session_state.get("chat_messages", []):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question about this video..."):
        st.session_state["chat_messages"].append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            reply = st.session_state["chatbot"].ask(prompt)
        st.session_state["chat_messages"].append({"role": "assistant", "content": reply})
        st.rerun()
