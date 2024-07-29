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
st.title("Add A VERB Verb")
st.markdown(f"Hi {st.session_state.username}, You are currently logged with the role of {st.session_state.role}.")




#####################################################
#           Main Page                               #
#####################################################
verb = st.text_input("Verb")
singular_present = st.text_input("singular_present")
plural_form = st.text_input("plural_form")
past_singular = st.text_input("past_singular")
past_plural = st.text_input("past_plural")
perfect_participle = st.text_input("perfect_participle")
translation_en = st.text_input("English Translation")
translation_zh = st.text_input("Chinese Translation")
difficulty = st.selectbox("Difficulty", ['A1', 'A2', 'B1', 'B2', 'C1'])
if st.button("Save"):
    df = load_data(st.session_state.username, st.session_state.role, 'VERB')
    search_term_verb = verb.lower()
    search_term_singular_present = singular_present.lower()
    search_term_plural_form = plural_form.lower()
    search_term_past_singular = past_singular.lower()
    search_term_past_plural = past_plural.lower()
    search_term_perfect_participle = perfect_participle.lower()

    results = df[(df['verb'].str.lower() == search_term_verb) |
                (df['singular_present'].str.lower() == search_term_singular_present) |
                (df['plural_form'].str.lower() == search_term_plural_form) |
                (df['past_singular'].str.lower() == search_term_past_singular) |
                (df['past_plural'].str.lower() == search_term_past_plural) | 
                (df['perfect_participle'].str.lower() == search_term_perfect_participle)]

    if not results.empty:
        st.info(f"Word '{verb}' already exists in the database.")
        df.loc[results.index, 'search_count'] += 1
        if st.session_state.role == 'admin':
            df.loc[results.index, 'admin_search_count'] += 1
        st.dataframe(results, use_container_width=True)
        df.to_csv(f"{st.session_state.username}_VERB.csv", index=False)
    else:
        new_data = pd.DataFrame({
            'verb': [verb],
            'singular_present': [singular_present],
            'plural_form': [plural_form],
            'past_singular': [past_singular],
            'past_plural': [past_plural],
            'perfect_participle': [perfect_participle],
            'translation_en': [translation_en],
            'translation_zh': [translation_zh],
            'difficulty': [difficulty],
            'search_count': [0],
            'admin_search_count': [0]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(f"{st.session_state.username}_VERB.csv", index=False)
        st.write(f"Verb '{verb}' added to the database.")


