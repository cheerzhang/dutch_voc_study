import streamlit as st
import pandas as pd
import os

NOUN_CSV = 'dutch_words.csv'
VERB_CSV = 'dutch_verbs.csv'

# 初始化词汇 CSV 文件
if not os.path.exists(NOUN_CSV):
    df = pd.DataFrame(columns=['word', 'plural', 'gender', 'translation_en', 'translation_zh', 'difficulty', 'search_count'])
    df.to_csv(NOUN_CSV, index=False)

# 初始化动词 CSV 文件
if not os.path.exists(VERB_CSV):
    df = pd.DataFrame(columns=['verb', 'plural', 'past_tense', 'past_participle', 'difficulty', 'search_count'])
    df.to_csv(VERB_CSV, index=False)

def load_data(csv_file):
    return pd.read_csv(csv_file)

def search_word(word, csv_file):
    df = load_data(csv_file)
    result = df[df['word'].str.lower() == word.lower()]
    if not result.empty:
        st.subheader("Search Results")
        st.dataframe(result)
        df.loc[result.index, 'search_count'] += 1
        df.to_csv(csv_file, index=False)
    else:
        st.write("Word not found.")

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
            'search_count': [0]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(NOUN_CSV, index=False)
        st.write(f"Word '{word}' added to the database.")

def search_verb(verb):
    df = load_data(VERB_CSV)
    result = df[df['verb'].str.lower() == verb.lower()]
    if not result.empty:
        st.subheader("Search Results")
        st.dataframe(result)
        df.loc[result.index, 'search_count'] += 1
        df.to_csv(VERB_CSV, index=False)
    else:
        st.write("Verb not found.")

def add_verb(verb, plural, past_tense, past_participle, difficulty):
    df = load_data(VERB_CSV)
    if verb.lower() in df['verb'].str.lower().values:
        st.write(f"Verb '{verb}' already exists in the database.")
    else:
        new_data = pd.DataFrame({
            'verb': [verb],
            'plural': [plural],
            'past_tense': [past_tense],
            'past_participle': [past_participle],
            'difficulty': [difficulty],
            'search_count': [0]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(VERB_CSV, index=False)
        st.write(f"Verb '{verb}' added to the database.")

def main():
    st.title("Dutch Vocabulary Learning Tool")

    menu = ["Search Noun",  "Add Noun", "View All Nouns",
            "Search Verb",  "Add Verb", "View All Verbs"]
    # choice = st.sidebar.selectbox("Menu", menu)
    choice = st.sidebar.radio("Menu", menu)

    if choice == "View All Nouns":
        st.subheader("All Noun in the Database")
        df = load_data(NOUN_CSV)
        st.dataframe(df)

    elif choice == "View All Verbs":
        st.subheader("All Verbs in the Database")
        df = load_data(NOUN_CSV)
        st.dataframe(df)

    elif choice == "Search Noun":
        st.subheader("Search Noun")
        word = st.text_input("Enter the Dutch word:")
        if st.button("Search"):
            search_word(word, NOUN_CSV)

    elif choice == "Search Verb":
        st.subheader("Search Verb")
        verb = st.text_input("Enter the Dutch verb:")
        if st.button("Search"):
            search_verb(verb)

    elif choice == "Add Noun":
        st.subheader("Add New Noun")
        word = st.text_input("Noun")
        plural = st.text_input("Plural")
        gender = st.selectbox("Gender", ['de', 'het'])
        translation_en = st.text_input("English Translation")
        translation_zh = st.text_input("Chinese Translation")
        difficulty = st.selectbox("Difficulty", ['A1', 'A2', 'B1', 'B2', 'C1'])
        
        if st.button("Save"):
            add_word(word, plural, gender, translation_en, translation_zh, difficulty)

    elif choice == "Add Verb":
        st.subheader("Add New Verb")
        verb = st.text_input("Verb")
        plural = st.text_input("Plural")
        past_tense = st.text_input("Past Tense")
        past_participle = st.text_input("Past Participle")
        difficulty = st.selectbox("Difficulty", ['A1', 'A2', 'B1', 'B2', 'C1'])
        
        if st.button("Save"):
            add_verb(verb, plural, past_tense, past_participle, difficulty)

if __name__ == "__main__":
    main()
