import app_setup  # noqa
import os
from jose import jwt
import streamlit as st
from auth0_component import login_button

st.write("Page 1")

try:
    auth = login_button(
        clientId=os.getenv("clientId"),
        domain=os.getenv("domain"),
        audience=os.getenv("audience"),
        issuer=os.getenv("issuer"),
        debug_logs=os.getenv("debug_logs"),
    )
except jwt.ExpiredSignatureError:
    st.warning("Your session expired. Please login again.")
    auth = None
except jwt.JWTClaimsError as e:
    st.warning(f"There was an issue with your claims: {e}")
    auth = None
except Exception as e:
    st.warning(f"An unknow error occurred when authenticating: {e}")
    auth = None

if auth:
    st.write(auth)
    st.metric(label="Temp", value="273 K", delta="1.2 K")

    st.checkbox('I like cheese', key="likes_cheese")
    st.checkbox('Chocolate and peanut butter should not be paired', key="ultimate_truth")
