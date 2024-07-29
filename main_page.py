import streamlit as st
import hashlib
import json, os
import pandas as pd

# 示例用户数据
users = {
    "admin": {
        "password": "75836b220eaf45c58c6e030620a6b5853bd1fc1021f7b74ec3150644918a8bd8", 
        "role": "admin"},
    "user1": {
        "password": "75836b220eaf45c58c6e030620a6b5853bd1fc1021f7b74ec3150644918a8bd8", 
        "role": "admin"}
}

# 验证用户
def authenticate_user(username, password):
    if username in users:
        stored_password_hash = users[username]['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        st.write(password_hash)
        return stored_password_hash == password_hash
    return False

# 登录函数
def login():
    st.session_state['authenticated'] = False
    st.session_state['username'] = 'guest'
    st.session_state['role'] = 'guest'

    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.session_state['role'] = users[username]['role']
                st.success("Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    with col2:
        if st.button("Continue as Guest"):
            st.session_state['authenticated'] = True
            st.session_state['username'] = "guest"
            st.session_state['role'] = "guest"
            st.success("Continuing as guest.")
            st.experimental_rerun()

# 主应用程序
def main():
    # 初始化 session state
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        st.session_state['username'] = 'guest'
        st.session_state['role'] = 'guest'

    # 登录/游客模式选择
    if not st.session_state['authenticated']:
        login()
    else:
        st.sidebar.title(f"Welcome, {st.session_state['username']}!")
        if st.sidebar.button("Logout"):
            st.session_state['authenticated'] = False
            st.session_state['username'] = 'guest'
            st.session_state['role'] = 'guest'
            st.success("Logged out successfully!")
            st.experimental_rerun()

        st.title("Dutch Vocabulary Learning Tool")

        # 根据角色显示不同的菜单
        if st.session_state['role'] == 'admin':
            menu = ["Search", "Add", "View"]
        else:
            menu = ["Search", "View"]

        choice = st.sidebar.radio("Menu", menu)

        if choice == "Search":
            st.subheader("Search Functionality")
            st.write("This is the search functionality.")
            # 添加搜索功能的代码
        elif choice == "Add" and st.session_state['role'] == 'admin':
            st.subheader("Add Functionality")
            st.write("This is the add functionality.")
            # 添加添加单词功能的代码
        elif choice == "View":
            st.subheader("View Functionality")
            st.write("This is the view functionality.")
            # 添加查看所有单词功能的代码
            if os.path.exists("guest_NOUN.csv"):
                df_guest_n = pd.read_csv("guest_NOUN.csv")
                st.dataframe(df_guest_n, use_container_width=True)
                # 提供下载功能
                csv_guest_n = df_guest_n.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download noun data as CSV",
                    data=csv_guest_n,
                    file_name="guest_NOUN.csv",
                    mime='text/csv',
                )
            else:
                st.error(f"File 'guest_NOUN.csv' not found.")
            if os.path.exists("guest_VERB.csv"):
                df_guest_v = pd.read_csv("guest_VERB.csv")
                st.dataframe(df_guest_v, use_container_width=True)
                # 提供下载功能
                csv_guest_v = df_guest_v.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download verb data as CSV",
                    data=csv_guest_v,
                    file_name="guest_VERB.csv",
                    mime='text/csv',
                )
            else:
                st.error(f"File 'guest_VERB.csv' not found.")

if __name__ == "__main__":
    main()
    
    