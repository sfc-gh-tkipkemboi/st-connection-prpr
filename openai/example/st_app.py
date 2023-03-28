import streamlit as st
from openai_connection import connect_openai

st.title("ChatGPT AMA")
conn = connect_openai()
input = st.text_input("Ask your question:")
if input:
    st.info(conn.get_completion(input))

# messages = [{"role": "user", "content": "Hi ChatGPT. How is your day going?"}]
# response = chat_completion(messages)

# st.write(response)

# rmsg = response.choices[0].message.content

# st.write(rmsg)
