import streamlit as st
import pandas as pd
from utils.words_action import load_guest_data, load_user_data
from menu import menu_with_redirect
import os

#####################################################
#             Page Control                          #
#####################################################
st.set_option("client.showSidebarNavigation", False)
menu_with_redirect()
if st.session_state.role not in ["admin", "guest"]:
    st.warning("You do not have permission to view this page. This function is only for registed user.")
    st.stop()
st.title("View All Noun or Verb Words.")
st.markdown(f"Hi {st.session_state.username}, You are currently logged with the role of {st.session_state.role}.")



#############################################
#             Page                          #
#############################################
if st.session_state.role == 'guest':
    st.write(f"Current working directory: {os.getcwd()}")
    df_n = pd.read_csv(f"guest_NOUN.csv")
    st.dataframe(df_n)
    df_v = load_guest_data('VERB')
    
    st.subheader("All Nouns in the Database")
    st.dataframe(df_n, use_container_width=True)
    csv_n = df_n.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Nouns as CSV",
        data=csv_n,
        file_name=f"{st.session_state.username}_NOUN.csv",
        mime='text/csv',
    )
    
    st.subheader("All Verbs in the Database")
    st.dataframe(df_v, use_container_width=True)
    csv_v = df_v.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Verbs as CSV",
        data=csv_v,
        file_name=f"{st.session_state.username}_VERB.csv",
        mime='text/csv',
    )
elif st.session_state.role == 'admin':
    df_1, df_2 = load_user_data(st.session_state.username, 'NOUN')
    df_2 = df_1.merge(
        df_2[['word', 'admin_search_count']], 
        on='word', 
        how='left', 
        suffixes=('', '_y')
    )
    df_2 = df_2[['word', 'plural', 'gender', 'translation_en', 'translation_zh', 'difficulty', 'search_count', 'admin_search_count']]
    df_2['admin_search_count'] = df_2['admin_search_count'].fillna(0)
    df_n = df_2.copy()
    
    st.subheader("All Nouns in the Database")
    st.dataframe(df_n, use_container_width=True)
    csv_n = df_n.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Nouns as CSV",
        data=csv_n,
        file_name=f"{st.session_state.username}_NOUN.csv",
        mime='text/csv',
    )

    df_1_, df_2_ = load_user_data(st.session_state.username, 'VERB')
    st.dataframe(df_2_)
    df_2_ = df_1_.merge(
        df_2_[['verb', 'admin_search_count']], 
        on='verb', 
        how='left', 
        suffixes=('', '_y')
    )
    df_2_ = df_2_[['verb', 'singular_present', 'plural_form', 'past_singular', 'past_plural', 'perfect_participle', 'translation_en', 'translation_zh', 'difficulty', 'search_count', 'admin_search_count']]
    df_2_['admin_search_count'] = df_2_['admin_search_count'].fillna(0)
    df_v = df_2_.copy()
    st.subheader("All Verbs in the Database")
    st.dataframe(df_v, use_container_width=True)
    csv_v = df_v.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Verbs as CSV",
        data=csv_v,
        file_name=f"{st.session_state.username}_VERB.csv",
        mime='text/csv',
    )




