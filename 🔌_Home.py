import streamlit as st

st.set_page_config(
    page_title='st.connection PrPr',
    page_icon='🔌'
)

st.title("🔌 st.connection Private Preview")

"""
**Welcome to the st.connection preview!**

**st.connection** makes it easy to connect your Streamlit apps to data, with a fraction of the code.

* The full PR is [here](https://github.com/streamlit/streamlit/pull/6035).
* 👉 **Try it out yourself** with the latest .whl file from [here](https://core-previews.s3-us-west-2.amazonaws.com/pr-6035/streamlit-1.17.0-py2.py3-none-any.whl).
"""

with st.expander("🎈 Watch the feature walkthrough video 🎈"):
    "*For the quick version just watch the first two minutes* 🙂"
    st.markdown("""
    <iframe src="https://drive.google.com/file/d/19xNGTLPxMCLHaRXaJbEqEAV60TvEQgXC/preview" width="640" height="480" allow="autoplay" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs([
    "🚀 With st.connection",
    "🐢 Compare to today"
])

with tab1:
    st.code("""
import streamlit as st

conn = st.connection('sql')
df = conn.read_sql('select * from pet_owners')
st.dataframe(df)
    """, language='python'
    )

with tab2:
    "Sourced from [Streamlit's MySQL tutorial](https://docs.streamlit.io/knowledge-base/tutorials/databases/mysql#write-your-streamlit-app)"

    st.code("""
import streamlit as st
import mysql.connector

@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from pet_owners;")
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
""", language='python'
    )

"""
st.connection includes:

- `st.connection()` factory method to initialize ready-to-use data connection objects
- Concrete implementations in Streamlit for a few key data sources:
  - SQL engines including Postgresql, MySQL, sqlite, MS SQL Server, Snowflake, Oracle, BigQuery, Redshift and
[more](https://docs.sqlalchemy.org/en/14/dialects/index.html)
  - Cloud file storage including S3, GCS, ABS, FTP, HDFS, and [more](https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations)
  - Snowpark for Snowflake
- An extendable `BaseConnection` class to easily build (and share) new connection types!
"""

"""
👈 Check out the supported connection types, view the detailed docs, and send us your feedback!

**This preview is shared for feedback purposes only and is not intended for any production-like use.**
"""
