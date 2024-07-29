import streamlit as st
import pandas as pd
import os


NOUN_CSV = 'dutch_words.csv'
VERB_CSV = 'dutch_verbs.csv'

def load_data(csv_file, role, data_type='NOUN'):
    if not os.path.exists(csv_file):
        if data_type == 'NOUN':
            df = pd.DataFrame(columns=['word', 'plural', 'gender', 'translation_en', 'translation_zh', 'difficulty', 'search_count', 'admin_search_count'])
        if data_type == 'VERB':
            df = pd.DataFrame(columns=['verb', 'singular_present', 'plural_form', 'past_singular', 'past_plural', 'perfect_participle', 'translation_en', 'translation_zh', 'difficulty', 'search_count'])
        df.to_csv(csv_file, index=False)
    df = pd.read_csv(csv_file)
    if role == 'guest':
        return df
    elif role == 'admin':
        if 'admin_search_count' not in df.columns:
            df['admin_search_count'] = 0
        return df

#########################################
#         Add Nouns                     #
#########################################
def add_word(word, plural, gender, translation_en, translation_zh, difficulty):
    df = load_data(NOUN_CSV)
    if word.lower() in df['word'].str.lower().values:
        st.write(f"Word '{word}' already exists in the database.")
    else:
        new_data = pd.DataFrame({
            'word': [word],
            'plural': [plural],
            'gender': [gender],
            'translation_en': [translation_en],
            'translation_zh': [translation_zh],
            'difficulty': [difficulty],
            'search_count': [0],
            'admin_search_count': [0]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(NOUN_CSV, index=False)
        st.write(f"Word '{word}' added to the database.")

def add_verb(verb, singular_present, plural_form, past_singular, past_plural, perfect_participle, translation_en, translation_zh, difficulty):
    df = load_data(VERB_CSV)
    if verb.lower() in df['verb'].str.lower().values:
        st.write(f"Verb '{verb}' already exists in the database.")
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
        df.to_csv(VERB_CSV, index=False)
        st.write(f"Verb '{verb}' added to the database.")



#################################
#         search                #
#################################
def search_word_data(word):
    df = load_data(NOUN_CSV)
    search_term = word.lower()
    # 在所有列中搜索
    results = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search_term).any(), axis=1)]
    
    if not results.empty:
        st.subheader("Word Search Results")
        st.dataframe(results[['word', 'plural', 'gender', 'translation_en', 'translation_zh', 'difficulty', 'search_count', 'admin_search_count']], use_container_width=True)
        # 增加搜索次数
        df.loc[results.index, 'search_count'] += 1
        if st.session_state['is_admin']:
            df.loc[results.index, 'admin_search_count'] += 1
        df.to_csv(NOUN_CSV, index=False)
    else:
        st.write("No matching word found.")


def search_verb_data(verb):
    df = load_data(VERB_CSV)
    search_term = verb.lower()
    # 在所有列中搜索
    results = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search_term).any(), axis=1)]
    
    if not results.empty:
        st.subheader("Verb Search Results")
        st.dataframe(results[['verb', 'singular_present', 'plural_form', 'past_singular', 'past_plural', 'perfect_participle', 'translation_en', 'translation_zh', 'difficulty', 'search_count', 'admin_search_count']], use_container_width=True)
        # 增加搜索次数
        df.loc[results.index, 'search_count'] += 1
        if st.session_state['is_admin']:
            df.loc[results.index, 'admin_search_count'] += 1
        df.to_csv(VERB_CSV, index=False)
    else:
        st.write("No matching verb found.")