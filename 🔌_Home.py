import streamlit as st

st.set_page_config(
    page_title='st.connection PrPr',
    page_icon='🔌'
)

st.title("🔌 st.connection Private Preview")

"""
**Welcome to the st.connection preview!**

* The full PR is [here](https://github.com/streamlit/streamlit/pull/6035).
* 👉 **Try it out yourself** with the latest .whl file from [here](https://core-previews.s3-us-west-2.amazonaws.com/pr-6035/streamlit-1.17.0-py2.py3-none-any.whl).
"""

st.code("""
import streamlit as st

conn = st.connection('sql')
df = conn.read_sql('select * from pet_owners')
st.dataframe(df)
""", language='python'
)

"""
**st.connection** makes it easy to write Streamlit apps with high quality data connections.
The feature includes:

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
