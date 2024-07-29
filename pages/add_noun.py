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
word = st.text_input("Noun")
plural = st.text_input("Plural")
gender = st.selectbox("Gender", ['de', 'het'])
translation_en = st.text_input("English Translation")
translation_zh = st.text_input("Chinese Translation")
difficulty = st.selectbox("Difficulty", ['A1', 'A2', 'B1', 'B2', 'C1'])
if st.button("Save"):
    df = load_data(st.session_state.username, st.session_state.role, 'NOUN')
    search_term_word = word.lower()
    search_term_plural = plural.lower()
    results = df[(df['word'].str.lower() == search_term_word) | 
                 (df['plural'].str.lower() == search_term_plural)]
    if not results.empty:
        st.info(f"Word '{word}' already exists in the database.")
        df.loc[results.index, 'search_count'] += 1
        if st.session_state.role == 'admin':
            df.loc[results.index, 'admin_search_count'] += 1
        st.dataframe(results, use_container_width=True)
        df.to_csv(f"{st.session_state.username}_NOUN.csv", index=False)
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
        df.to_csv(f"{st.session_state.username}_NOUN.csv", index=False).encode('utf-8')
        # also saved in normal
        new_data = pd.DataFrame({
            'word': [word],
            'plural': [plural],
            'gender': [gender],
            'translation_en': [translation_en],
            'translation_zh': [translation_zh],
            'difficulty': [difficulty],
            'search_count': [0]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(f"guest_NOUN.csv", index=False).encode('utf-8')
        st.info(f"Word '{word}' added to the database.")

