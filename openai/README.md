# Streamlit OpenAI Connection

A prototype OpenAI Connection for st.connection in Streamlit.

## Minimal working example

```python
# st_app.py

import streamlit as st
from streamlit_openai import connect_openai

st.title("ChatGPT AMA")
conn = connect_openai()
input = st.text_input("Ask your question:")
if input:
    st.info(conn.get_completion(input))
```

```toml
# .streamlit/secrets.toml

[connections.openai]
api_key = "<your api key>"

# A few other optional params can be added here or in kwargs
# but only api_key is required. E.g.
model = "text-davinci-003"
```

```txt
# requirements.txt

streamlit==1.20
git+https://github.com/sfc-gh-jcarroll/st-connection-prpr.git#subdirectory=openai
```

## Currently supported methods

- `get_completion(prompt: str) -> str`: Get a completion (text) for the provided prompt.
- `get_embedding(text: str) -> Sequence[float]`: Get an embedding vector (list of floats) for the provided text.
- `client() -> ModuleType`: Get the underlying OpenAI client (which is an initialized module).

Everything is Streamlit cached by default.
