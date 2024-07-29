import streamlit as st
import pandas as pd
from utils.words_action import load_guest_data, load_user_data
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
    if st.session_state.role == 'guest':
        df_n = load_guest_data('NOUN')
    elif st.session_state.role == 'admin':
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
    results = df_n[(df_n['word'].str.lower() == search_term_word) | 
                 (df_n['plural'].str.lower() == search_term_word)]
    if not results.empty:
        st.subheader("Word Search Results In Noun")
        # st.dataframe(results, use_container_width=True)
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
    
    # try searching in verb
    if st.session_state.role == 'guest':
        df_v = load_guest_data('VERB')
    elif st.session_state.role == 'admin':
        df_v, df_v_user = load_user_data(st.session_state.username, 'VERB')
        df_v_user = df_v.merge(
            df_v_user[['verb', 'admin_search_count']], 
            on='verb', 
            how='left', 
            suffixes=('', '_y')
        )
        df_v_user = df_v_user[['verb', 'singular_present', 'plural_form', 'past_singular', 'past_plural', 'perfect_participle', 'translation_en', 'translation_zh', 'difficulty', 'search_count', 'admin_search_count']]
        df_v_user['admin_search_count'].fillna(0, inplace=True)

    search_term = word.lower()
    results = df_v[(df_v['verb'].str.lower() == search_term) |
                (df_v['singular_present'].str.lower() == search_term) |
                (df_v['plural_form'].str.lower() == search_term) |
                (df_v['past_singular'].str.lower() == search_term) |
                (df_v['past_plural'].str.lower() == search_term) | 
                (df_v['perfect_participle'].str.lower() == search_term)]
    if not results.empty:
        st.subheader("Word Search Results In Verb")
        df_v.loc[results.index, 'search_count'] += 1
        df_v.to_csv(f"guest_VERB.csv", index=False)
        if st.session_state.role == 'admin':
            df_v_user.loc[results.index, 'admin_search_count'] += 1
            df_v_user.to_csv(f"{st.session_state.username}_VERB.csv", index=False)
            st.dataframe(df_v_user.loc[results.index], use_container_width=True)
        if st.session_state.role == 'guest':
            st.dataframe(df_v.loc[results.index], use_container_width=True)
    else:
        st.info("No matching word found in verb.")

