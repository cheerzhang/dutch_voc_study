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
st.title("View All Noun or Verb Words.")
st.markdown(f"Hi {st.session_state.username}, You are currently logged with the role of {st.session_state.role}.")



#############################################
#             Page                          #
#############################################
NOUN_CSV_USER = f"{st.session_state.username}_Noun.csv"
VERB_CSV_USER = f"{st.session_state.username}_Verb.csv"

st.subheader("All Nouns in the Database")
df_n = load_data(NOUN_CSV_USER, st.session_state.role, 'NOUN')
st.dataframe(df_n, use_container_width=True)
csv_n = df_n.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Nouns as CSV",
    data=csv_n,
    file_name=NOUN_CSV_USER,
    mime='text/csv',
)

st.subheader("All Verbs in the Database")
df_v = load_data(VERB_CSV_USER, st.session_state.role, 'VERB')
st.dataframe(df_v, use_container_width=True)
csv_v = df_v.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Nouns as CSV",
    data=csv_v,
    file_name=VERB_CSV_USER,
    mime='text/csv',
)

