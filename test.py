import streamlit as st
import os, json
from menu import menu
import hashlib


st.set_option("client.showSidebarNavigation", False)

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = "guest"
st.session_state._role = st.session_state.role


def set_role():
    st.session_state.role = st.session_state._role


st.title("Login or Continue as Guest")
username = st.text_input("Username", disabled=False if st.session_state.role is "guest" else True)
password = st.text_input("Password", type="password", disabled=False if st.session_state.role is None else True)

    
# Create a login button
if st.button("Login", disabled = False if st.session_state.role is "guest" else False):
    with open('.localDB/db.json') as f:
        users = json.load(f)
    if username in users.keys():
        password_store = users[username]['password']
        password_hash = hashlib.sha256(password.encode() + b'salt').hexdigest()
        if password_hash == password_store:
            st.success("Logged in as {}".format(username))
            st.session_state.username = username
            st.session_state.disabled = True
            st.session_state.role = users[username]['role']
        else:
            st.error("Invalid username or password")
    else:
        st.error("Invalid username or password")
if st.button("Log Out", disabled = True if st.session_state.role is "guest" else False):
    st.session_state.username = "guest"
    st.session_state.disabled = False
    st.session_state.role = "guest"
    st.success("Logged out. Please refresh the page and login in again.")
if st.button("Continue as guest"):
    st.session_state.username = "guest"
    st.session_state.disabled = False
    st.session_state.role = "guest"
    st.success("Switched to the guest account. Please refresh the page and login in again.")
menu() # Render the dynamic menu!

