import streamlit as st
import pandas as pd
import os
import hashlib
from utils.words_action import load_data, add_verb, add_word, search_verb_data, search_word_data

NOUN_CSV = 'dutch_words.csv'
VERB_CSV = 'dutch_verbs.csv'

# 初始化词汇 CSV 文件
if not os.path.exists(NOUN_CSV):
    df = pd.DataFrame(columns=['word', 'plural', 'gender', 'translation_en', 'translation_zh', 'difficulty', 'search_count', 'admin_search_count'])
    df.to_csv(NOUN_CSV, index=False)

# 初始化动词 CSV 文件
if not os.path.exists(VERB_CSV):
    df = pd.DataFrame(columns=['verb', 'singular_present', 'plural_form', 'past_singular', 'past_plural', 'perfect_participle', 'translation_en', 'translation_zh', 'difficulty', 'search_count', 'admin_search_count'])
    df.to_csv(VERB_CSV, index=False)


def is_authenticated(username, password):
    stored_password_hash = '0964e974ef82cb613a246de50c20171ec7182c2ad2322d1c2d3f2fc850ccb0d5'
    password_hash = hashlib.sha256(password.encode() + b'salt').hexdigest()
    return username == 'admin' and password_hash == stored_password_hash

def main():
    st.title("Dutch Vocabulary Learning Tool")

    # 检查并设置 session_state 变量
    if 'is_admin' not in st.session_state:
        st.session_state['is_admin'] = False

    # 用户认证
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.button("Login"):
        if is_authenticated(username, password):
            st.session_state['is_admin'] = True
            st.success("Login successful")
        else:
            st.session_state['is_admin'] = False
            st.error("Login failed")

    menu = ["Search Noun", "Add Noun", "View All Nouns", "Search Verb", "Add Verb", "View All Verbs"]
    choice = st.sidebar.radio("Menu", menu)

    if choice == "View All Nouns":
        st.subheader("All Nouns in the Database")
        df = load_data(NOUN_CSV)
        st.dataframe(df)
        if st.session_state['is_admin']:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Nouns as CSV",
                data=csv,
                file_name='dutch_words.csv',
                mime='text/csv',
            )

    elif choice == "View All Verbs":
        st.subheader("All Verbs in the Database")
        df = load_data(VERB_CSV)
        st.dataframe(df)
        if st.session_state['is_admin']:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Verbs as CSV",
                data=csv,
                file_name='dutch_verbs.csv',
                mime='text/csv',
            )

    elif choice == "Search Noun":
        st.subheader("Search Noun")
        word = st.text_input("Enter the Dutch word:")
        if st.button("Search"):
            search_word_data(word)
    
    elif choice == "Search Verb":
        st.subheader("Search Verb")
        verb = st.text_input("Enter the Dutch verb:")
        if st.button("Search"):
            search_verb_data(verb)

    elif choice == "Add Noun" and st.session_state['is_admin']:
        st.subheader("Add New Noun")
        word = st.text_input("Noun")
        plural = st.text_input("Plural")
        gender = st.selectbox("Gender", ['de', 'het'])
        translation_en = st.text_input("English Translation")
        translation_zh = st.text_input("Chinese Translation")
        difficulty = st.selectbox("Difficulty", ['A1', 'A2', 'B1', 'B2', 'C1'])
        
        if st.button("Save"):
            if not search_word_data(word):
                add_word(word, plural, gender, translation_en, translation_zh, difficulty)
            else:
                st.info(f"{word} has already been in the noun DB")

    elif choice == "Add Verb" and st.session_state['is_admin']:
        st.subheader("Add New Verb")
        verb = st.text_input("Verb")
        singular_present = st.text_input("singular_present")
        plural_form = st.text_input("plural_form")
        past_singular = st.text_input("past_singular")
        past_plural = st.text_input("past_plural")
        perfect_participle = st.text_input("perfect_participle")
        translation_en = st.text_input("English Translation")
        translation_zh = st.text_input("Chinese Translation")
        difficulty = st.selectbox("Difficulty", ['A1', 'A2', 'B1', 'B2', 'C1'])
        if st.button("Save"):
            if not search_verb_data(verb):
                add_verb(verb, singular_present, plural_form, past_singular, past_plural, perfect_participle, translation_en, translation_zh, difficulty)
            else:
                st.info(f"{verb} has already been in the verb DB")

if __name__ == "__main__":
    main()
