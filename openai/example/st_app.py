import streamlit as st
from streamlit_openai import connect_openai

st.title("ChatGPT AMA")
conn = connect_openai()
input = st.text_input("Ask your question:")
if input:
    st.info(conn.get_completion(input))
