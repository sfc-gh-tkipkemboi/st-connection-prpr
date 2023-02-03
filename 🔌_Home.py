import streamlit as st

st.set_page_config(
    page_title='st.connection PrPr',
    page_icon='🔌'
)

st.title("🔌 st.connection PrPr [WIP]")

"""
**Landing page and demo for the st.connection Private Preview.**

* The full PR is [here](https://github.com/streamlit/streamlit/pull/6035).
* Install the latest .whl file from [here](https://core-previews.s3-us-west-2.amazonaws.com/pr-6035/streamlit-1.17.0-py2.py3-none-any.whl).
"""

st.code("""
import streamlit as st

conn = st.connection('sql')
df = conn.read_sql('select * from pet_owners')
st.dataframe(df)
""", language='python'
)

"""
👈 Check out the supported connection types, view the detailed docs, and send us your feedback!
"""
