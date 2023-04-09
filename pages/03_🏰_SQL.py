import streamlit as st

from datetime import timedelta

st.set_page_config(
    page_title='st.connection for SQL',
    page_icon='🏰'
)


def _repr_html_(self) -> str:
    module_name = getattr(self, "__module__", None)
    class_name = type(self).__name__
    if self._connection_name:
        name = f"`{self._connection_name}` "
        if len(self._secrets) > 0:
            cfg = f"""- Configured from `[connections.{self._connection_name}]`
            """
        else:
            cfg = ""
    else:
        name = ""
        cfg = ""
    # TODO: Make the dialect line more robust (e.g. figure it out from URL if needed, maybe include driver too)
    md = f"""
    ---
    **st.connection {name}built from `{module_name}.{class_name}`**
    {cfg}
    - Dialect: `{self._secrets.dialect}`
    - Learn more using `st.help()`
    ---
    """
    return md

st.title('🏰 st.connection for SQL')

connection_secrets = """
# .streamlit/secrets.toml
[connections.pets_db]
url = "sqlite:///pets.db"
"""

st.subheader("Init")

"""
Initialize the connection:
"""
with st.echo():
    conn = st.experimental_connection('pets_db', type='sql')
    st.write(_repr_html_(conn))

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
            
st.subheader("query() for common cases")

"""
For a typical use case where you just need to query and cache some data, it's much simpler.
Just use `conn.query()`. By default it caches the result without expiration, or you can add a TTL.
This also support parameters, pagination, date conversions, etc (see the full docs).

By default, `query()` returns a `pandas.DataFrame`. We also intend to easily support other common
return formats, like `pyarrow.Table`.
"""

with st.echo():
    pet_owners = conn.query('select * from pet_owners', ttl=timedelta(minutes=10))
    st.dataframe(pet_owners)
