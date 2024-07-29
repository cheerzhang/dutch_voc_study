import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("test.py", label="LogIn Page")
    if st.session_state.role in ["admin", "guest"]:
        st.sidebar.page_link("pages/add_noun.py", label="[Noun]Add", disabled=st.session_state.role not in ["admin"])
        st.sidebar.page_link("pages/add_verb.py", label="[Verb]Add", disabled=st.session_state.role not in ["admin"])
        st.sidebar.page_link("pages/search_word.py", label="[Noun+Verb]Search", disabled=st.session_state.role not in ["admin", "guest"])
        st.sidebar.page_link("pages/view_word.py", label="[Noun+Verb]View All", disabled=st.session_state.role not in ["admin", "guest"])
        

def unauthenticated_menu():
    st.sidebar.page_link("test.py", label="Log in")


def menu():
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("test.py")
    menu()
        