import streamlit as st

from datetime import timedelta

st.set_page_config(
    page_title='st.connection PrPr - SQL',
    page_icon='🔌'
)

st.title('🔌 st.connection PrPr - SQL')

st.markdown("""
See the <a href='/Detailed_Docs#sql-connection' target='_self'>Detailed Docs</a> for quickstart, install instructions and the full API reference.

**To run it yourself, do `pip install SQLAlchemy` and install the driver library for your [SQL Dialect](https://docs.sqlalchemy.org/en/20/dialects/index.html).**
""", unsafe_allow_html=True)

connection_secrets = """
# .streamlit/secrets.toml
[connections.sql]
url = "sqlite:///mydb.db"
"""

st.subheader("Init")

"Initialize and view the connection:"

with st.echo():
    conn = st.connection('sql')

    conn

"secrets.toml looks like this:"
st.code(connection_secrets, language='toml')

st.subheader("Use session() for writes and transactions")

"""
`conn.session()` returns an underlying SQLAlchemy Session that can be used for writes,
transactions, using the SQLAlchemy ORM and other more advanced operations.
"""

with st.echo():
    with conn.session() as s:
        st.markdown(f"Note that `s` is a `{type(s)}`")
        s.execute('CREATE TABLE IF NOT EXISTS pet_owners (person TEXT, pet TEXT);')
        s.execute('DELETE FROM pet_owners;')
        pet_owners = {'jerry': 'fish', 'barbara': 'cat', 'alex': 'puppy'}
        for k in pet_owners:
            s.execute(
                'INSERT INTO pet_owners (person, pet) VALUES (:owner, :pet);',
                params=dict(owner=k, pet=pet_owners[k])
            )
        s.commit()
            
st.subheader("read_sql() for common cases")

"""
For a typical use case where you just need to query and cache some data, it's much simpler.
Just use `conn.read_sql()` and get a dataframe back. By default it caches the result without
expiration, or you can add a TTL. This also support parameters, pagination, date conversions,
etc (see the full docs).
"""

with st.echo():
    df = conn.read_sql('select * from pet_owners', ttl=timedelta(minutes=10))
    st.dataframe(df)

