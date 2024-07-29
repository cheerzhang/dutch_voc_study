import streamlit as st
import os, json
from menu import menu
import hashlib


st.set_option("client.showSidebarNavigation", False)

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = "guest"
if "username" not in st.session_state:
    st.session_state.username = "guest"
st.session_state._role = st.session_state.role


def set_role():
    st.session_state.role = st.session_state._role


st.title("Login or Continue as Guest")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

    
# Create a login button
col_left, col_right = st.columns(2)
with col_left:
    if st.button("Login"):
        with open('.localDB/db.json') as f:
            users = json.load(f)
        if username in users.keys():
            password_store = users[username]['password']
            password_hash = hashlib.sha256(password.encode() + b'salt').hexdigest()
            if password_hash == password_store:
                st.success("Logged in as {}".format(username))
                st.session_state.username = username
                st.session_state.role = users[username]['role']
            else:
                st.error("Invalid user, Please continue as the guest account")
        else:
            st.error("Invalid user, Please continue as the guest account")
with col_right:
    if st.button("Continue (Switch) as guest"):
        st.session_state.username = "guest"
        st.session_state.role = "guest"
        st.success("Switched to the guest account.")
menu() # Render the dynamic menu!

