import streamlit as st

st.set_page_config(
    page_title='st.connection PrPr',
    page_icon='🔌'
)

st.title("🔌 st.connection PrPr")

"A simple landing page and demo app for st.connection"

st.markdown("This app is running on [this commit](https://github.com/streamlit/streamlit/tree/e3737e3bd1372e7cd288b4529ec72eaf1089b966).")

st.markdown("Check out the .whl file [here](). **TODO: NEED TO ADD**")

with st.expander("Sample usage"):
    "secrets.toml looks like this:"
    code = """
[connections.sql]
url = "sqlite:///mydb.db"
    """
    st.code(code, language='toml')

    "Here's the example code:"
    
    with st.echo():
        conn = st.connection('sql')

        conn


    with st.echo():
        # Grab a SQLAlchemy engine and insert some data in a transaction
        c = conn.instance.connect()
        c.execute('CREATE TABLE IF NOT EXISTS pet_owners (person TEXT, pet TEXT);')
        c.execute('DELETE FROM pet_owners;')
        pet_owners = {'jerry': 'fish', 'barbara': 'cat', 'alex': 'puppy'}
        for k in pet_owners:
            c.execute('INSERT INTO pet_owners (person, pet) VALUES (:owner, :pet);', owner=k, pet=pet_owners[k])
                

    with st.echo():
        # Let's see how it worked!
        df = conn.read_sql('select * from pet_owners', ttl_minutes=1)
        st.dataframe(df)
