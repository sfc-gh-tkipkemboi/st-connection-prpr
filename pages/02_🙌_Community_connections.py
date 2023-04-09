import streamlit as st

st.set_page_config(
    page_title='Community connections',
    page_icon='🙌'
)

st.title("🙌 Community connections")

"""
We're excited for the community to extend and build on the st.connection interface and make it easier than ever to build Streamlit apps
with a wide variety of data sources. We've built the interface with this in mind. To use a community-built connection in your Streamlit app,
you just need to install and import it, then pass the class to st.connection(), like this:

```python
import streamlit as st
# We haven't actually built this one yet... want to help? ;)
from streamlit_extras.gspread_connection import GSpreadConnection

conn = st.experimental_connection("pets_gsheet", GSpreadConnection)
pet_owners = conn.get_worksheet("pet_owners")
st.dataframe(pet_owners)
```

These type of connections work exactly the same as the ones built into Streamlit and have access to all the same capabilities.
"""
