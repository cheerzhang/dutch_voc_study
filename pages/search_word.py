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
NOUN_CSV_USER = f"{st.session_state.username}_Noun.csv"
VERB_CSV_USER = f"{st.session_state.username}_Verb.csv"
word = st.text_input("Enter the Dutch word:")
if st.button("Search"):
    # try searching in noun
    df = load_data(NOUN_CSV_USER, st.session_state.role, 'NOUN')
    search_term = word.lower()
    results = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search_term).any(), axis=1)]
    if not results.empty:
        st.subheader("Word Search Results In Noun")
        st.dataframe(results, use_container_width=True)
        df.loc[results.index, 'search_count'] += 1
        if st.session_state.role == 'admin':
            df.loc[results.index, 'admin_search_count'] += 1
        df.to_csv(NOUN_CSV_USER, index=False)
    else:
        st.info("No matching word found in noun.")
    
    # try searching in verb
    df = load_data(VERB_CSV_USER, st.session_state.role, 'VERB')
    search_term = word.lower()
    results = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search_term).any(), axis=1)]
    if not results.empty:
        st.subheader("Word Search Results In Verb")
        st.dataframe(results, use_container_width=True)
        df.loc[results.index, 'search_count'] += 1
        if st.session_state.role == 'admin':
            df.loc[results.index, 'admin_search_count'] += 1
        df.to_csv(VERB_CSV_USER, index=False)
    else:
        st.info("No matching word found in verb.")

