import streamlit as st

st.set_page_config(
    page_title='st.connection PrPr - Docs',
    page_icon='🔌'
)

st.title('🔌 st.connection PrPr - Docs')

st.code("""
import streamlit as st

conn = st.connection('sql')
df = conn.read_sql('select * from pet_owners')
st.dataframe(df)
""", language='python'
)

"""
**st.connection** makes it easy to write Streamlit apps with high quality data connections:
fast, reliable, secure, portable and intuitive. The feature includes:

* `st.connection()` factory method to initialize ready-to-use data connection objects
* Concrete implementations in Streamlit for a few key data sources: SQL, cloud file storage, and Snowpark
* An extendable `BaseConnection` class to easily build (and share) new connection types!
"""

st.subheader("Table of Contents")

"""
- [st.connection() function](#st-connection-function)
- [Built-in SQL Connection](#built-in-sql-connection)
  - [Configuration parameters](#configuration-parameters-sql)
  - [st.connection() arguments](#st-connection-arguments)
  - [read_sql()](#read-sql-sql)
  - [session()](#session-sql)
- [Built-in Files Connection](#built-in-files-connection)
  - [Configuration parameters](#configuration-parameters-sql)
  - [open()](#open)
  - [read_*()](#read)
  - [conn.instance](#conn-instance)
- [Built-in Snowpark Connection](#built-in-snowpark-connection)
  - [Configuration parameters](#configuration-parameters-snowpark)
  - [session()](#session-snowpark)
  - [read_sql()](#read-sql-snowpark)
- [BaseConnection and building your own](#baseconnection-and-building-your-own)

"""

st.header('`st.connection()` function')

"""
`st.connection(connection_class → Literal[str] or Class = None, name → str =’default’, **kwargs)`

Create and return a connection object based on the provided class and referenced connection configuration.

**Parameters**

- **connection_class** *(Literal[str] or Class)* - Required. The class of Connection to create.
  - First party connections included in Streamlit core can be referenced by string name (`’sql'`)
  - Otherwise the actual (imported) class should be provided. Classes must extend `BaseConnection` (detailed below).
- **name** *(str)* - Keyword-only parameter. The name of the connection.
    - st.connection will look up config in `[connections.<name>]` in `.streamlit/secrets.toml`
    - If left as ‘default’, it will use the `default_connection_name` from the `connection_class`
- **kwargs** - Additional arguments passed to the connection, the same as specifying them in secrets.toml under the connections block.

```python
import streamlit as st

conn = st.connection('sql', name='userdb', autocommit=True)
```

```python
import streamlit as st
from duckdb_connection import DuckDBConnection

conn = st.connection(DuckDBConnection)
```
"""

st.subheader('Built-in SQL Connection')

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

st.markdown("""
See the <a href='/SQL' target='_self'>SQL page</a> for full usage examples.

The SQL connection (`streamlit.connections.SQL`) is built on [SQLAlchemy](https://docs.sqlalchemy.org/en/14/). It supports
connecting to Snowflake, Postgresql, MySQL, sqlite, MS SQL Server, Oracle, BigQuery, Redshift and
[more](https://docs.sqlalchemy.org/en/14/dialects/index.html). To use it, you will need to install SQLAlchemy as well as
any needed engine-specific drivers.
""", unsafe_allow_html=True)

st.code("""
import streamlit as st

conn = st.connection('sql', name='userdb', autocommit=True)
df = conn.read_sql('select * from pet_owners')
st.dataframe(df)
""", language='python'
)

"""
#### Configuration parameters (SQL)

You can include the following in your `secrets.toml` under `[connections.<connection name>]`

* `url`: Should follow the [SQLAlchemy database URLs syntax](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls).
Other connection definition parameters can be omitted and will be ignored if this is included.
This syntax also supports additional key/value query arguments being passed.
* `dialect`: The SQL dialect, such as postgresql, mysql, sqlite, snowflake, etc
* `driver`: the name of the driver package to use. Will use the dialect default if omitted.
* `username`, `password`, `host`, `database`, `port`: The usual SQL parameters 😃

#### st.connection() arguments

SQL also supports:

* `autocommit` - Whether to enable autocommit for sessions, if the dialect supports it
* `**kwargs` - Any additional keyword arguments which are passed directly to
[sqlalchemy.create_engine()](https://docs.sqlalchemy.org/en/14/core/engines.html#sqlalchemy.create_engine).

### read_sql() (SQL)

`conn.read_sql()` is the most common function to use, for an app that simply needs to query some data
from the database and then perform further operations on it.

`read_sql(self, sql: str, ttl: Optional[Union[float, int, timedelta]] = None. **kwargs) -> pd.DataFrame)`

Run the provided SQL query on the underlying connection, optionally cache the result, and return it as a pandas DataFrame.

**Parameters**

- **sql** *(str)* - Required. The SQL query to execute. Allows bound parameters.
- **ttl** *(int, float, or datetime.timedelta)* - How long to cache the result. By default, it does not expire.
- **kwargs** - Additional arguments. `params` is the most common to include, but supports the same arguments as
[pd.read_sql()](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html).

```python
df = conn.read_sql('select * from pet_owners', ttl=timedelta(minutes=10))
st.dataframe(df)
```

#### session() (SQL)

Call `conn.session()` to get the underlying
[SQLAlchemy Session](https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session).
This can be useful for interacting with SQLAlchemy's ORM or committing basic write/update operations.

```python
with conn.session() as s:
    s.execute('CREATE TABLE IF NOT EXISTS pet_owners (person TEXT, pet TEXT);')
    s.execute(
        'INSERT INTO pet_owners (person, pet) VALUES (:owner, :pet);',
        params=dict(owner='jerry', pet='fish')
    )
    s.commit()
```

"""


st.subheader('Built-in Files Connection')

st.markdown("""
See the <a href='/Files' target='_self'>Files page</a> for full usage examples.

The Files connection (`streamlit.connections.FileSystem`) is built on [fsspec](https://filesystem-spec.readthedocs.io/en/latest/?badge=latest).
It supports connecting to S3, GCS, ABS, local files, FTP, HDFS, git and
[more](https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations). To use it, you will need to install fsspec as well as
any needed file system-specific drivers.
""", unsafe_allow_html=True)

st.code("""
import streamlit as st

conn = st.connection('s3')
df = conn.read_csv('my-bucket/pet_owners.csv')
st.dataframe(df)
""", language='python'
)

"""
#### Configuration parameters (Files)

You can include the following in your `secrets.toml` under `[connections.<connection name>]`:

- `protocol`: specifies the file system protocol, like `'s3'` or `'gcs'`
- protocol specific configuration - see the docs for the relevant protocol

Many protocols can also be configured using the standard ways, such as `AWS_ACCESS_KEY` ENV, GCS token, `~/.aws/credentials`, etc.
The connection object will detect and configure using these if available.

**Quick initialization:**
- `st.connection('files', protocol=...)` - the default approach, checks for config in `[connections.files]`
- `st.connection('s3', ...)` - this is equivalent to `st.connection('files', name='s3', protocol='s3', ...)`
- `st.connection('gcs', ...)` - this is equivalent to `st.connection('files', name='gcs', protocol='gcs', ...)`

#### open()

Open a file at the provided path. Accepts all the usual arguments.

```python
with conn.open("my-bucket/pet-log.txt", "wt") as f:
    f.write("Barbara owns a cat.")
```

#### read_*()

FileSystem connection also supports the following methods:
- read_text() -> str
- read_bytes() -> bytes
- read_csv() -> pd.DataFrame
- read_parquet() -> pd.DataFrame

Each of these will open and read a file at the provided path, optionally cache the results (using `ttl=`), and return it in the specified format.

```python
df = conn.read_csv("my-bucket/pet_owners.csv")
st.dataframe(df)
```

#### conn.instance

`conn.instance` returns an [fsspec.spec.AbstractFileSystem](https://filesystem-spec.readthedocs.io/en/latest/api.html#fsspec.spec.AbstractFileSystem)
for a fuller set of file operations.

```python
pet_logs = conn.instance.ls("my-pets-bucket/")
st.write(pet_logs)
```

"""

st.subheader('Built-in Snowpark Connection')

st.markdown("""
See the <a href='/Snowpark' target='_self'>Snowpark page</a> for full usage examples.

The Snowpark connection (`streamlit.connections.Snowpark`) is built on [snowpark-python](https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html).
To use it, you will need to install snowpark-python and have access to a Snowflake account.
""", unsafe_allow_html=True)

"""
#### Configuration parameters (Snowpark)

Configuration can be provided in `secrets.toml` under `[connections.snowpark]` (or your custom connection name). The connection will also check
for credentials in `~/.snowsql/config` (as [here](https://docs.snowflake.com/en/user-guide/snowsql-start.html#configuring-default-connection-settings))
if none is found in `secrets.toml`. It supports
[all the normal Snowflake connection parameters](https://docs.snowflake.com/en/user-guide/python-connector-api.html#label-snowflake-connector-methods).

**Not yet supported, but coming soon:**
- Support for configuration from ENV
- Detection of running in Streamlit-in-Snowflake (where available) and automatic configuration

#### session() (Snowpark)

Most common for an in-depth use case, use `conn.session()` to retrieve the Snowpark Session and get access to the full Snowpark DataFrame API.

```python
with conn.session() as session:
    pets_df = session.table('pet_owners')
    pets_df = pets_df.filter(col('PET_COUNT') > 1)

st.dataframe(pets_df)
```

#### read_sql() (Snowpark)

For quick usage or if all computation will be specified in SQL, you can use the convenience `read_sql()` method. It returns a pandas DataFrame
which by default is cached by Streamlit.

```python
df = conn.read_sql('select * from pet_owners', ttl=timedelta(minutes=10))
st.dataframe(df)
```

"""

st.header('`BaseConnection` and building your own')

"""
You can import `streamlit.connections.BaseConnection` into your own packages to develop new Connection
types for use with Streamlit. `BaseConnection` provides a standard API for init and lifecycle, so that
your class works well with `st.connection()` and Streamlit caching. You can also extend your Connection
class with convenience methods, but we recommend doing this sparingly!

Below, find the key elements of a custom Connection using a simple example writing a connection for DuckDB.

```python
from streamlit.connections import BaseConnection
import duckdb

class DuckDBConnection(BaseConnection[duckdb.DuckDBPyConnection]):
    _default_connection_name = "duckdb"
```

Note that this class:
* extends `BaseConnection`
* specifies the underlying connection object, `duckdb.DuckDBPyConnection`
* specifies the `_default_connection_name = "duckdb"`, meaning these connections will look in
`[connections.duckdb]` for secrets and connection parameters by default

```python
def connect(self, **kwargs) -> duckdb.DuckDBPyConnection:
    self._closed = False

    if 'database' in kwargs:
        db = kwargs.pop('database')
        return duckdb.connect(database=db, **kwargs)

    secrets = self.get_secrets()
    return duckdb.connect(secrets['database'], **kwargs)
```

Implementing `connect()` is the key function for any connection class. This is called by `st.connection()`
whenever a new connection object is needed.

```python
def disconnect(self) -> None:
    self.instance.close()
    self._closed = True

def is_connected(self) -> bool:
    return not self._closed
```

`disconnect()` and `is_connected()` are used by Streamlit lifecycle to keep your connection healthy and active.

**That's it!** You've implemented a minimal connection. As mentioned above, you might want to add some
more convenience methods to make it easier for app developers to interact with this connection.
See a full example [here](https://github.com/sfc-gh-jcarroll/st-connection-prpr/blob/main/duckdb_connection/connection.py).
"""