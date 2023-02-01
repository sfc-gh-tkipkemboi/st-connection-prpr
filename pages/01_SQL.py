import streamlit as st

from datetime import timedelta

st.set_page_config(
    page_title='st.connection PrPr - SQL',
    page_icon='🔌'
)

st.title('🔌 st.connection PrPr - SQL')

st.markdown("""
See the <a href='/Detailed_Docs#sql-connection' target='_self'>Detailed Docs</a> for quickstart, install instructions and the full API reference.
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

st.subheader("Use the raw instance")

with st.echo():
    # `instance` provides the underlying object - in this case a SQLAlchemy Engine
    st.markdown(f"`conn.instance` is a `{type(conn.instance)}`")

with st.echo():
    # Grab a SQLAlchemy Session and insert some data
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
            
st.subheader("`read_sql()` convenience method")
with st.echo():
    # Let's see how it worked!
    df = conn.read_sql('select * from pet_owners', ttl=timedelta(minutes=10))
    st.dataframe(df)

