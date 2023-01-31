import streamlit as st

from datetime import timedelta

st.set_page_config(
    page_title='st.connection PrPr - SQL',
    page_icon='🔌'
)

st.title('🔌 st.connection PrPr - SQL')

with st.expander("Quickstart / Install instructions - SQL"):
    st.subheader("Dependencies")
    """
    To run the st.connection PrPr you need the following installed:
    * **The custom whl file (linked above)**
    * **SQLAlchemy** `pip install SQLAlchemy` - recommend version 1.4 or 2.0
    * **[DBAPI Driver](https://docs.sqlalchemy.org/en/20/dialects/index.html) for your database engine** - e.g. `psycopg2` for Postgres, `mysqlclient` for MySQL, etc. SQLite is already installed.

    We plan to add features in the future that will make it easier to manage these extra installs.
    """

    st.subheader("Configuration and secrets")
    """
    You also need to add a `[connections.sql]` section in your `.streamlit/secrets.toml` and fill in the configuration, like the usage example below. [More info on Streamlit secrets.toml here](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management).

    Here's a minimal example:
    """
    connection_secrets = """
# .streamlit/secrets.toml
[connections.sql]
url = "sqlite:///mydb.db"
    """
    st.code(connection_secrets, language='toml')

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
        st.markdown(f"Note that `c` is a `{type(s)}`")
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
