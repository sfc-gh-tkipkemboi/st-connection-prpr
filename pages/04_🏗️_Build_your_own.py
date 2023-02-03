import streamlit as st

st.set_page_config(
    page_title='st.connection PrPr - Build your own',
    page_icon='🔌'
)

st.title('🔌 st.connection PrPr - Build your own')

"""
st.connection makes it easy to build, use and share your own connection implementations.

To demonstrate this, this app has a simple [DuckDB](https://duckdb.org/) Connection built in.
You can view the connection source code
[here](https://github.com/sfc-gh-jcarroll/st-connection-prpr/blob/main/duckdb_connection/connection.py).
"""

with st.echo():
    from duckdb_connection import DuckDBConnection

    conn = st.connection(DuckDBConnection, database=':memory:')
    conn

"Let's insert some data with the underlying duckdb cursor"
with st.echo():
    c = conn.cursor()
    # create a table
    c.execute("CREATE TABLE IF NOT EXISTS items(item VARCHAR, value DECIMAL(10,2), count INTEGER)")
    # drop any existing data from a prior run ;)
    c.execute("DELETE FROM items")
    # insert two items into the table
    c.execute("INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)")
    # insert a row using prepared statements
    c.execute("INSERT INTO items VALUES (?, ?, ?)", ['laptop', 2000, 1])

"Now check out the awesome convenience method!"

with st.echo():
    df = conn.read_duck("select * from items")
    st.dataframe(df)
