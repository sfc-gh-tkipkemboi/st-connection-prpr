# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from contextlib import contextmanager
from datetime import timedelta
from io import TextIOWrapper
from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Optional, Union, overload
from typing_extensions import Literal

import pandas as pd

from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

if TYPE_CHECKING:
    from fsspec import AbstractFileSystem, filesystem
    from fsspec.spec import AbstractBufferedFile


class FilesConnection(ExperimentalBaseConnection["AbstractFileSystem"]):

    def __init__(
        self, connection_name: str = "default", protocol: str | None = None, **kwargs
    ) -> None:
        self.protocol = protocol
        super().__init__(connection_name, **kwargs)

    def _connect(self, **kwargs) -> "AbstractFileSystem":
        """
        Pass a protocol such as "s3", "gcs", or "file"
        """
        from fsspec import AbstractFileSystem, filesystem
        from fsspec.spec import AbstractBufferedFile

        secrets = self._secrets.to_dict()
        protocol = secrets.pop("protocol", self.protocol)

        if protocol is None:
            protocol = "file"

        if protocol == "gcs" and secrets:
            secrets = {"token": secrets}

        if self.protocol is None:
            self.protocol = protocol
        
        secrets.update(kwargs)

        fs = filesystem(protocol, **secrets)

        return fs
    
    @property
    def client(self) -> "AbstractFileSystem":
        return self._instance

    @contextmanager
    def open(
        self, path: str | Path, mode: str = "rb", *args, **kwargs
    ) -> Iterator[TextIOWrapper | AbstractBufferedFile]:
        # Connection name is only passed to make sure that the cache is
        # connection-specific
        if "connection_name" in kwargs:
            kwargs.pop("connection_name")

        with self.client.open(path, mode, *args, **kwargs) as f:
            yield f

    @overload
    def read(
        self,
        path: str | Path,
        input_format: Literal["text"],
        ttl: Optional[Union[float, int, timedelta]] = None,
        **kwargs,
    ) -> str:
        pass

    @overload
    def read(
        self,
        path: str | Path,
        input_format: Literal["csv"],
        ttl: Optional[Union[float, int, timedelta]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        pass

    @overload
    def read(
        self,
        path: str | Path,
        input_format: Literal["parquet"],
        ttl: Optional[Union[float, int, timedelta]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        pass

    def read(
        self,
        path: str | Path,
        input_format: str = None,
        ttl: Optional[Union[float, int, timedelta]] = None,
        **kwargs,
    ):
        @cache_data(ttl=ttl)
        def _read_text(path: str | Path, **kwargs) -> str:
            if "connection_name" in kwargs:
                kwargs.pop("connection_name")

            with self.open(path, "rt", **kwargs) as f:
                return f.read()

        @cache_data(ttl=ttl)
        def _read_csv(path: str | Path, **kwargs) -> pd.DataFrame:
            if "connection_name" in kwargs:
                kwargs.pop("connection_name")

            with self.open(path, "rt") as f:
                return pd.read_csv(f, **kwargs)

        @cache_data(ttl=ttl)
        def _read_parquet(path: str | Path, **kwargs) -> pd.DataFrame:
            if "connection_name" in kwargs:
                kwargs.pop("connection_name")

            with self.open(path, "rb") as f:
                return pd.read_parquet(f, **kwargs)
        
        if input_format == 'text':
            return _read_text(path, connection_name=self._connection_name, **kwargs)
        elif input_format == 'csv':
            return _read_csv(path, connection_name=self._connection_name, **kwargs)
        elif input_format == 'parquet':
            return _read_parquet(path, connection_name=self._connection_name, **kwargs)
        # TODO: if input_format is None, try to infer it from file extension
        raise ValueError(f"{input_format} is not a valid value for `input_format=`.")

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
        md = f"""
        ---
        **st.connection {name}built from `{module_name}.{class_name}`**
        {cfg}
        - Protocol: `{self.protocol}`
        - Learn more using `st.help()`
        ---
        """
        return md
