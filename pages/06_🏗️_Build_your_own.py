import streamlit as st

st.set_page_config(
    page_title='Build your own connection',
    page_icon='🏗️'
)

st.title('🏗️ Build your own connection')

"""
st.connection makes it easy to build, use and share your own connection implementations.

"""

# """
# To demonstrate this, this app has a simple [DuckDB](https://duckdb.org/) Connection built in.
# You can view the connection source code
# [here](https://github.com/sfc-gh-jcarroll/st-connection-prpr/blob/main/duckdb_connection/connection.py).
# """

"""
1. Create a new connection class that extends Streamlit's BaseConnection. It also needs the type
of the underlying connection object to be specified.

```python
from streamlit.connections import BaseConnection
import duckdb

class DuckDBConnection(BaseConnection[duckdb.DuckDBPyConnection])
```

2. Add a `connect()` method that sets up and returns the underlying connection object. It can pull
secrets specific to the connection from the `self._secrets` property.

```python
def _connect(self, **kwargs) -> duckdb.DuckDBPyConnection:
    if 'database' in kwargs:
        db = kwargs.pop('database')
    else:
        db = self._secrets['database']
    return duckdb.connect(database=db, **kwargs)
```

3. Add a way to get the underlying connection object. BaseConnection has a `_instance` property that does this
by default. Most connections will want some domain-specific property or method that exposes this.

```python
def cursor(self) -> duckdb.DuckDBPyConnection:
    return self._instance.cursor()
```

4. Add any convenience read / getter methods. These should be wrapped with @st.cache_data by default,
and conform to the st.connection best practices (see below).

```python
def query(self, query: str, ttl: int = 3600, **kwargs) -> pd.DataFrame:
    @cache_data(ttl=ttl)
    def _query(query: str, **kwargs) -> pd.DataFrame:
        cursor = self.cursor()
        cursor.execute(query, **kwargs)
        return cursor.df()
    
    return _query(query, **kwargs)
```

**:tada: That's it! You've implemented a minimal Connection class that is ready to be used with st.connection. :balloon:**
"""

with st.expander("To show it's that easy, see the DuckDB code running here :rocket:"):
    """
    You can view the DuckDB connection source code
    [here](https://github.com/sfc-gh-jcarroll/st-connection-prpr/blob/main/duckdb_connection/connection.py).
    """

    with st.echo():
        from duckdb_connection import DuckDBConnection

        conn = st.experimental_connection("duckdb", type=DuckDBConnection, database=':memory:')
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
        df = conn.query("select * from items")
        st.dataframe(df)

"""
## [Draft! Feedback welcome!] Best Practices for Connections

### Read / Get  methods

We expect the most frequent use case for Connection objects will be straightforward data reads or GET calls to an API. We recommend the following:

- Is wrapped by `st.cache_data` by default
- Use simple required arguments, an optional `ttl` argument for caching, and any other optional arguments that users may expect or commonly use in a “pareto 80%” use case.
- Return either:
    - For tabular data: a `pandas.DataFrame` or a `pyarrow.Table`
    - For document / object data: a dict-like object (typical default today - we want to find a pattern to expose the "core" response as well)
    - More discussion on this below 👇
- Handles errors or stale connections with the reset/retry pattern described below.

**Method naming**

We're debating the best way to name these methods. Currently leaning towards:
- single verbs for data sources / tabular data (`read()`, `query()`, etc)
- `get_noun()` for REST-API style connections
  - Alternate ideas would just be `get()` with the object/endpoint as an argument, or `noun()`

**Method return values**

We think it's useful to have some flexibility in this.
- For a quick data science prototype, `pandas.DataFrame` can work great.
- More modern / performance sensitive developers may want `pyarrow.Table`, especially if the underlying data source supports it natively
- An API can have REST, streaming response, etc; developer may also just want the "core" response (e.g. the text an LLM gives back) without the wrapping object
- In some cases, you may want a lazy-evaluated result / future object (although we haven't figured out how to auto-cache these effectively yet)

For the initial launch, we will probably pick a type: for tabular data, encourage returning pandas DF or arrow Table.

For (near) future, one idea is to have a `format='pandas'` argument that can have a default set in the connection class, be overridden in class
construction and/or be set in specific method calls, and have the class know how to convert from the "default" format to any other supported formats.
This could also possibly take a Callable that handles the conversion and returns the desired custom format. What do you think?

### Handling stale connections

Connection objects are cached in Streamlit by default. In some cases, an underlying connection may unexpectedly stop working (such as due to OAuth token expiring,
connection being closed on the server side, etc). To handle this case, BaseConnection provides a `reset()` method to re-create the connection object.

If the underlying connection package you are using is subject to this issue, we recommend to wrap any provided read methods with some kind of retry logic
(such as provided by [tenacity](https://tenacity.readthedocs.io/en/latest/index.html)) and reset the connection in the case of a call that fails due to some
transient issue. You can find some reference examples in the provided connections from Streamlit. You may also consider exposing a simple way for app developers
using the underlying connection to access the same functionality (we're still experimenting internally with the best way to do this).

Other clients may be more robust to this issue (by auto-refreshing tokens, handling server-side closure etc) and not require handling this issue as part of
st.connection.
"""
