from streamlit.connections import BaseConnection
from streamlit.runtime.caching import cache_data

import duckdb
import pandas as pd

class DuckDBConnection(BaseConnection[duckdb.DuckDBPyConnection]):
    _default_connection_name = "duckdb"

    def connect(self, **kwargs) -> duckdb.DuckDBPyConnection:
        self._closed = False

        if 'database' in kwargs:
            db = kwargs.pop('database')
            return duckdb.connect(database=db, **kwargs)

        secrets = self.get_secrets()
        return duckdb.connect(secrets['database'], **kwargs)

    def disconnect(self) -> None:
        self.instance.close()
        self._closed = True

    def is_connected(self) -> bool:
        return not self._closed

    @staticmethod
    def _read_duck(query: str, _instance: duckdb.DuckDBPyConnection, **kwargs) -> pd.DataFrame:
        _instance.execute(query, **kwargs)
        return _instance.df()

    def read_duck(self, query: str, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        instance = self.instance.cursor()
        if ttl:
            return cache_data(self._read_duck, ttl=ttl)(
                query, instance, **kwargs
            )
        return self._read_duck(query, instance, **kwargs)

    def cursor(self) -> duckdb.DuckDBPyConnection:
        return self._instance.cursor()
