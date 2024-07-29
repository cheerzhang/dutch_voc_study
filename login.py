import streamlit as st
import hashlib

def is_authenticated(username, password):
    stored_password_hash = 'your_precomputed_hash_here'  # 替换为实际计算出的哈希值
    password_hash = hashlib.sha256(password.encode() + b'salt').hexdigest()
    return username == 'admin' and password_hash == stored_password_hash

def login_page():
    if 'is_admin' not in st.session_state:
        st.session_state['is_admin'] = None

    if st.session_state['is_admin'] is None:
        # 初始登录页面
        st.subheader("Login or Continue as Guest")
        login_choice = st.selectbox("Choose an option", ["Guest", "Login as Admin"])
        if login_choice == "Login as Admin":
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            if st.button("Login"):
                if is_authenticated(username, password):
                    st.session_state['is_admin'] = True
                    st.success("Login successful")
                else:
                    st.session_state['is_admin'] = False
                    st.error("Login failed")
        elif login_choice == "Guest":
            if st.button("Continue as Guest"):
                st.session_state['is_admin'] = False

    return 'admin' if st.session_state['is_admin'] else 'guest'
