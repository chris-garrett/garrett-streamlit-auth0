import os
import time
import streamlit as st
from auth0_component import login_button

st.write("Page 2")

try:
    auth = login_button(
        clientId=os.getenv("clientId"),
        domain=os.getenv("domain"),
        audience=os.getenv("audience"),
        issuer=os.getenv("issuer"),
        debug_logs=os.getenv("debug_logs"),
    )
except Exception as e:
    st.write(f"Auth failed {type(e)} {e}")
    auth = None

if auth:
    st.write(auth)
    st.balloons()
    btn = st.button("click me")
    if btn:
        st.session_state["clicked"] = time.time()
