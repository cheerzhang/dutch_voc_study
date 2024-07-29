import streamlit as st
import hashlib


# 明文密码和盐的组合
password = "...."
salt = "salt"

# 计算哈希值
def cal_hash(text):
    password_hash = hashlib.sha256(password.encode() + salt.encode()).hexdigest()
    st.write(password_hash)
    return password_hash