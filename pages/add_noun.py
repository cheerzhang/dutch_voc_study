import streamlit as st
import pandas as pd
from utils.words_action import load_data
from menu import menu_with_redirect


#####################################################
#             Page Control                          #
#####################################################
st.set_option("client.showSidebarNavigation", False)
menu_with_redirect()
if st.session_state.role not in ["admin"]:
    st.warning("You do not have permission to view this page. This function is only for registed user.")
    st.stop()
st.title("Add A Noun Verb")
st.markdown(f"Hi {st.session_state.username}, You are currently logged with the role of {st.session_state.role}.")




#####################################################
#           Main Page                               #
#####################################################
NOUN_CSV_USER = f"{st.session_state.username}_Noun.csv"
word = st.text_input("Noun")
plural = st.text_input("Plural")
gender = st.selectbox("Gender", ['de', 'het'])
translation_en = st.text_input("English Translation")
translation_zh = st.text_input("Chinese Translation")
difficulty = st.selectbox("Difficulty", ['A1', 'A2', 'B1', 'B2', 'C1'])
if st.button("Save"):
    df = load_data(NOUN_CSV_USER, st.session_state.role, 'NOUN')
    search_term_word = word.lower()
    search_term_plural = plural.lower()
    word_exists = df[df['word'].str.lower() == search_term_word]
    plural_exists = df[df['plural'].str.lower() == search_term_plural]
    if not word_exists.empty or not plural_exists.empty:
        st.info(f"Word '{word}' or plural '{plural}' already exists in the database.")
        if not word_exists.empty:
            df.loc[word_exists.index, 'search_count'] += 1
            if st.session_state.role == 'admin':
                df.loc[word_exists.index, 'admin_search_count'] += 1
            st.dataframe(word_exists, use_container_width=True)
        if not plural_exists.empty:
            df.loc[plural_exists.index, 'search_count'] += 1
            if st.session_state.role == 'admin':
                df.loc[plural_exists.index, 'admin_search_count'] += 1
            st.dataframe(plural_exists, use_container_width=True)
        df.to_csv(NOUN_CSV_USER, index=False)
    else:
        new_data = pd.DataFrame({
            'word': [word],
            'plural': [plural],
            'gender': [gender],
            'translation_en': [translation_en],
            'translation_zh': [translation_zh],
            'difficulty': [difficulty],
            'search_count': [0],
            'admin_search_count': [0]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(NOUN_CSV_USER, index=False)
        st.info(f"Word '{word}' added to the database.")

