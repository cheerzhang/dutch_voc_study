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
def display_data_page():
    if st.session_state.role == 'guest':
        if os.path.exists("guest_VERB.csv"):
            df_v = pd.read_csv("guest_VERB.csv")
        else:
            df_v = pd.DataFrame(columns=['verb', 'singular_present', 'plural_form', 'past_singular', 'past_plural', 'perfect_participle', 'translation_en', 'translation_zh', 'difficulty', 'search_count'])
            df_v.to_csv("guest_VERB.csv", index=False)
        st.subheader("All Verbs in the Database")
        st.dataframe(df_v, use_container_width=True)
        csv_v = df_v.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Verb as CSV",
            data=csv_v,
            file_name="guest_VERB.csv",
            mime='text/csv',
        )


#####################################################
#             Main Function                         #
#####################################################

def main():
    display_data_page()

if __name__ == "__main__":
    main()