import app_setup  # noqa
import os
import streamlit as st
from auth0_component import login_button

st.write("Page 1")
auth = login_button(
    clientId=os.getenv("clientId"),
    domain=os.getenv("domain"),
    audience=os.getenv("audience"),
    issuer=os.getenv("issuer"),
    debug_logs=os.getenv("debug_logs")
)
if auth:
    st.write(auth)
    st.metric(label="Temp", value="273 K", delta="1.2 K")
