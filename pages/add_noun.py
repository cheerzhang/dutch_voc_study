import streamlit as st
import pandas as pd
from utils.words_action import load_user_data
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
    df_n, df_n_user = load_user_data(st.session_state.username, 'NOUN')
    df_n_user = df_n.merge(
            df_n_user[['word', 'admin_search_count']], 
            on='word', 
            how='left', 
            suffixes=('', '_y')
        )   
    df_n_user = df_n_user[['word', 'plural', 'gender', 'translation_en', 'translation_zh', 'difficulty', 'search_count', 'admin_search_count']]
    df_n_user['admin_search_count'].fillna(0, inplace=True)
    
    search_term_word = word.lower()
    search_term_plural = plural.lower()
    results = df_n[(df_n['word'].str.lower() == search_term_word) | 
                 (df_n['plural'].str.lower() == search_term_plural)]
    if not results.empty:
        st.subheader("Word Search Results In Noun")
        df_n.loc[results.index, 'search_count'] += 1
        df_n.to_csv(f"guest_NOUN.csv", index=False)
        if st.session_state.role == 'admin':
            df_n_user.loc[results.index, 'admin_search_count'] += 1
            df_n_user.to_csv(f"{st.session_state.username}_NOUN.csv", index=False)
            st.dataframe(df_n_user.loc[results.index], use_container_width=True)
        if st.session_state.role == 'guest':
            st.dataframe(df_n.loc[results.index], use_container_width=True)
    else:
        st.info("No matching word found in noun.")
        new_data = pd.DataFrame({
            'word': [word],
            'plural': [plural],
            'gender': [gender],
            'translation_en': [translation_en],
            'translation_zh': [translation_zh],
            'difficulty': [difficulty],
            'search_count': [0],
        })
        df = pd.concat([df_n, new_data], ignore_index=True)
        df.to_csv(f"guest_NOUN.csv", index=False)
        st.success(f"New word {word} added.")

