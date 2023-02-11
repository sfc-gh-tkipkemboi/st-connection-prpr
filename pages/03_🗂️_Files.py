import streamlit as st

import os
from tempfile import NamedTemporaryFile
import pandas as pd

st.set_page_config(
    page_title='st.connection PrPr - Files',
    page_icon='🔌'
)

st.title('🔌 st.connection PrPr - Files')

st.markdown("""
See the <a href='/Detailed_Docs#file-connection' target='_self'>Detailed Docs</a> for quickstart, install instructions and the full API reference.

**To run it yourself, do `pip install fsspec`. For authenticated cloud services, you'll also need to pip install the right driver:
`s3fs` for AWS S3, `gcsfs` for GCS, etc. See the full list of drivers
[here](https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations).**
""", unsafe_allow_html=True)

df = pd.DataFrame({"Owner": ["jerry", "barbara", "alex"], "Pet": ["fish", "cat", "puppy"], "Count": [4, 2, 1]})

local, s3, s3_other, gcs, gcs_other = st.tabs(
    [
        "Local files",
        "S3 files",
        "S3 files (other credentials)",
        "GCS files",
        "GCS files (other credentials)",
    ]
)
with local:
    st.write("## Working with local files")
    with st.echo():
        conn = st.connection('files')

    with st.expander("Setup code"):
        with st.echo():
            text_file = "test-files/test.txt"
            csv_file = "test-files/test.csv"
            parquet_file = "test-files/test.parquet"
            try:
                _ = conn.instance.ls("./test-files/")
            except FileNotFoundError:
                conn.instance.mkdir("./test-files/")
            try:
                _ = conn.read_text(text_file)
            except FileNotFoundError:
                with conn.open(text_file, "wt") as f:
                    f.write("This is a test")
            
            try:
                _ = conn.read_csv(csv_file)
            except FileNotFoundError:
                with conn.open(csv_file, "wt") as f:
                    df.to_csv(f, index=False)
            
            try:
                _ = conn.read_parquet(parquet_file)
            except FileNotFoundError:
                with conn.open(parquet_file, "wb") as f:
                    df.to_parquet(f)

    st.write("#### Text files")

    with st.echo():
        st.write(conn.read_text(text_file))

    st.write("#### CSV Files")
    with st.echo():
        st.write(conn.read_csv(csv_file))

    st.write("#### Parquet Files")
    with st.echo():
        st.write(conn.read_parquet(parquet_file))


with s3:
    st.write("## Working with S3 files")
    st.write("Credentials are stored in secrets.toml")

    st.code(
        """
# In secrets.toml
[connections.s3]
key = "..."
secret = "..."
    """,
        language="toml",
    )

    with st.echo():
        conn = st.connection('s3')

    with st.expander("Setup code"):
        with st.echo():
            text_file = "st-connection-test/test.txt"
            csv_file = "st-connection-test/test.csv"
            parquet_file = "st-connection-test/test.parquet"
            try:
                _ = conn.read_text(text_file)
            except FileNotFoundError:
                with conn.open(text_file, "wt") as f:
                    f.write("This is a test")
            
            try:
                _ = conn.read_csv(csv_file)
            except FileNotFoundError:
                with conn.open(csv_file, "wt") as f:
                    df.to_csv(f, index=False)
            
            try:
                _ = conn.read_parquet(parquet_file)
            except FileNotFoundError:
                with conn.open(parquet_file, "wb") as f:
                    df.to_parquet(f)

    st.write("#### Text files")

    with st.echo():
        st.write(conn.read_text(text_file))

    st.write("#### CSV Files")
    with st.echo():
        st.write(conn.read_csv(csv_file))

    st.write("#### Parquet Files")
    with st.echo():
        st.write(conn.read_parquet(parquet_file))
    
    st.write("#### List operations")
    with st.echo():
        st.write(conn.instance.ls("st-connection-test/"))

with s3_other:
    st.write("## Working with S3 files")

    # HACK to get the environment variables set
    secrets = st.secrets["connections"]["s3"]

    os.environ["AWS_ACCESS_KEY_ID"] = secrets["key"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = secrets["secret"]

    st.write(
        "Credentials stored in `~/.aws/config` or `AWS_ACCESS_KEY_ID` & "
        "`AWS_SECRET_ACCES_KEY` environment variables"
    )

    with st.echo():
        conn = st.connection('s3', name="s3-other")

    with st.expander("Setup code"):
        with st.echo():
            text_file = "st-connection-test/test2.txt"
            csv_file = "st-connection-test/test2.csv"
            parquet_file = "st-connection-test/test2.parquet"
            try:
                _ = conn.read_text(text_file)
            except FileNotFoundError:
                with conn.open(text_file, "wt") as f:
                    f.write("This is a test")
            
            try:
                _ = conn.read_csv(csv_file)
            except FileNotFoundError:
                with conn.open(csv_file, "wt") as f:
                    df.to_csv(f, index=False)
            
            try:
                _ = conn.read_parquet(parquet_file)
            except FileNotFoundError:
                with conn.open(parquet_file, "wb") as f:
                    df.to_parquet(f)

    st.write("#### Text files")
    with st.echo():
        st.write(conn.read_text(text_file))

    st.write("#### CSV Files")
    with st.echo():
        st.write(conn.read_csv(csv_file))

    st.write("#### Parquet Files")
    with st.echo():
        st.write(conn.read_parquet(parquet_file))
    
    st.write("#### List operations")
    with st.echo():
        st.write(conn.instance.ls("st-connection-test/"))


with gcs:
    st.write("## Working with Google Cloud Storage files")
    st.write("Credentials are set in secrets.toml")

    st.code(
        """
# In secrets.toml
[connections.gcs]
type = "..."
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n..."
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
    """,
        language="toml",
    )

    with st.echo():
        conn = st.connection('gcs')

    with st.expander("Setup code"):
        with st.echo():
            text_file = "st-connection-test/test3.txt"
            csv_file = "st-connection-test/test3.csv"
            parquet_file = "st-connection-test/test3.parquet"
            try:
                _ = conn.read_text(text_file)
            except FileNotFoundError:
                with conn.open(text_file, "wt") as f:
                    f.write("This is a test")
            
            try:
                _ = conn.read_csv(csv_file)
            except FileNotFoundError:
                with conn.open(csv_file, "wt") as f:
                    df.to_csv(f, index=False)
            
            try:
                _ = conn.read_parquet(parquet_file)
            except FileNotFoundError:
                with conn.open(parquet_file, "wb") as f:
                    df.to_parquet(f)

    st.write("#### Text files")

    with st.echo():
        st.write(conn.read_text(text_file))

    st.write("#### CSV Files")
    with st.echo():
        st.write(conn.read_csv(csv_file))

    st.write("#### Parquet Files")
    with st.echo():
        st.write(conn.read_parquet(parquet_file))
    
    st.write("#### List operations")
    with st.echo():
        st.write(conn.instance.ls("st-connection-test/"))

with gcs_other:
    "## Working with Google Cloud Storage files"
    st.write("Credentials are provided by a path to a service account json file")

    connection_details = dict(st.secrets["connections"]["gcs"])

    if "protocol" in connection_details:
        del connection_details["protocol"]

    with NamedTemporaryFile("w+", suffix=".json") as f:
        import json

        json.dump(connection_details, f)
        f.seek(0)

        credentials_file_name = f.name

        with st.echo():
            conn = st.connection('gcs', name="gcs-other", token=credentials_file_name)

        with st.expander("Setup code"):
            with st.echo():
                text_file = "st-connection-test/test4.txt"
                csv_file = "st-connection-test/test4.csv"
                parquet_file = "st-connection-test/test4.parquet"
                try:
                    _ = conn.read_text(text_file)
                except FileNotFoundError:
                    with conn.open(text_file, "wt") as f:
                        f.write("This is a test")
                
                try:
                    _ = conn.read_csv(csv_file)
                except FileNotFoundError:
                    with conn.open(csv_file, "wt") as f:
                        df.to_csv(f, index=False)
                
                try:
                    _ = conn.read_parquet(parquet_file)
                except FileNotFoundError:
                    with conn.open(parquet_file, "wb") as f:
                        df.to_parquet(f)

        st.write("#### Text files")

        with st.echo():
            st.write(conn.read_text(text_file))

        st.write("#### CSV Files")
        with st.echo():
            st.write(conn.read_csv(csv_file))

        st.write("#### Parquet Files")
        with st.echo():
            st.write(conn.read_parquet(parquet_file))
        
        st.write("#### List operations")
        with st.echo():
            st.write(conn.instance.ls("st-connection-test/"))