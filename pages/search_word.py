import streamlit as st
import pandas as pd
from utils.words_action import load_data
from menu import menu_with_redirect


#####################################################
#             Page Control                          #
#####################################################
st.set_option("client.showSidebarNavigation", False)
menu_with_redirect()
if st.session_state.role not in ["admin", "guest"]:
    st.warning("You do not have permission to view this page. This function is only for registed user.")
    st.stop()
st.title("Search A Noun or Verb Word.")
st.markdown(f"Hi {st.session_state.username}, You are currently logged with the role of {st.session_state.role}.")





#############################################
#             Page                          #
#############################################
word = st.text_input("Enter the Dutch word:")
if st.button("Search"):
    # try searching in noun
    df = load_data(st.session_state.username, st.session_state.role, 'NOUN')
    search_term_word = word.lower()
    results = df[(df['word'].str.lower() == search_term_word) | 
                 (df['plural'].str.lower() == search_term_word)]
    if not results.empty:
        st.subheader("Word Search Results In Noun")
        st.dataframe(results, use_container_width=True)
        df.loc[results.index, 'search_count'] += 1
        if st.session_state.role == 'admin':
            df.loc[results.index, 'admin_search_count'] += 1
        df.to_csv(f"{st.session_state.username}_NOUN.csv", index=False)
    else:
        st.info("No matching word found in noun.")
    
    # try searching in verb
    df = load_data(st.session_state.username, st.session_state.role, 'VERB')
    search_term = word.lower()
    results = df[(df['verb'].str.lower() == search_term) |
                (df['singular_present'].str.lower() == search_term) |
                (df['plural_form'].str.lower() == search_term) |
                (df['past_singular'].str.lower() == search_term) |
                (df['past_plural'].str.lower() == search_term) | 
                (df['perfect_participle'].str.lower() == search_term)]
    if not results.empty:
        st.subheader("Word Search Results In Verb")
        st.dataframe(results, use_container_width=True)
        df.loc[results.index, 'search_count'] += 1
        if st.session_state.role == 'admin':
            df.loc[results.index, 'admin_search_count'] += 1
        df.to_csv(f"{st.session_state.username}_VERB.csv", index=False)
    else:
        st.info("No matching word found in verb.")

