import streamlit as st
import pandas as pd
from menu import menu_with_redirect
import os

#####################################################
#             Page Control                          #
#####################################################




if "role" not in st.session_state:
    st.session_state.role = "guest"
if "username" not in st.session_state:
    st.session_state.username = "guest"
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
            df_v = pd.read_csv("guest_VERB.csv")
    if st.session_state.role == 'admin':
        if os.path.exists(f"guest_VERB.csv"):
            df_1 = pd.read_csv("guest_VERB.csv")
        else:
            df_1 = pd.DataFrame(columns=['verb', 'singular_present', 'plural_form', 'past_singular', 'past_plural', 'perfect_participle', 'translation_en', 'translation_zh', 'difficulty', 'search_count'])
            df_1.to_csv("guest_VERB.csv", index=False)
            df_1 = pd.read_csv("guest_VERB.csv")
        if os.path.exists(f"{st.session_state.username}_VERB.csv"):
            df_2 = pd.read_csv(f"{st.session_state.username}_VERB.csv")
        else:
            df_2 = df_1.copy()
            df_2['admin_search_count'] = 0
            df_2.to_csv(f"{st.session_state.username}_VERB.csv", index=False)
        df_2 = df_1.merge(
            df_2[['word', 'admin_search_count']], 
            on='word', 
            how='left', 
            suffixes=('', '_y')
        )
        df_2 = df_2[['word', 'plural', 'gender', 'translation_en', 'translation_zh', 'difficulty', 'search_count', 'admin_search_count']]
        df_2['admin_search_count'] = df_2['admin_search_count'].fillna(0)
        df_v = df_2.copy()
    return df_v


#####################################################
#             Main Function                         #
#####################################################

def main():
    st.set_option("client.showSidebarNavigation", False)
    menu_with_redirect()
    if st.session_state.role not in ["admin", "guest"]:
        st.warning("You do not have permission to view this page. This function is only for registed user.")
        st.stop()
    st.title("View All Noun or Verb Words.")
    st.markdown(f"Hi {st.session_state.username}, You are currently logged with the role of {st.session_state.role}.")

    df_v = display_data_page()
    st.subheader("All Verbs in the Database")
    st.dataframe(df_v, use_container_width=True)
    csv_v = df_v.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Verb as CSV",
        data=csv_v,
        file_name="guest_VERB.csv",
        mime='text/csv',
    )

if __name__ == "__main__":
    main()