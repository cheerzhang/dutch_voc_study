import streamlit as st
import pandas as pd
import os

CSV_FILE = 'dutch_words.csv'

# 如果文件不存在，创建一个新的CSV文件并写入表头
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['word', 'plural', 'gender', 'translation_en', 'translation_zh', 'difficulty', 'search_count'])
    df.to_csv(CSV_FILE, index=False)

def load_data():
    df = pd.read_csv(CSV_FILE)
    return df

def search_word(word):
    df = load_data()
    result = df[df['word'].str.lower() == word.lower()]
    if not result.empty:
        # 显示搜索结果
        st.subheader("Search Results")
        st.dataframe(result)
        # 更新搜索计数
        df.loc[result.index, 'search_count'] += 1
        df.to_csv(CSV_FILE, index=False)
    else:
        st.write("Word not found.")

def add_word(word, plural, gender, translation_en, translation_zh, difficulty):
    df = load_data()
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
        df.to_csv(CSV_FILE, index=False)
        st.write(f"Word '{word}' added to the database.")


def main():
    st.title("Dutch Vocabulary Learning Tool")

    menu = ["View All Words", "Search Word", "Add Word"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "View All Words":
        st.subheader("All Words in the Database")
        df = load_data()
        st.dataframe(df)

    elif choice == "Search Word":
        word = st.text_input("Enter the Dutch word:")
        if st.button("Search"):
            search_word(word)

    elif choice == "Add Word":
        st.subheader("Add New Word")
        word = st.text_input("Word")
        plural = st.text_input("Plural")
        gender = st.selectbox("Gender", ['de', 'het'])
        translation_en = st.text_input("English Translation")
        translation_zh = st.text_input("Chinese Translation")
        difficulty = st.selectbox("Difficulty", ['A1', 'A2', 'B1', 'B2', 'C1'])
        
        if st.button("Save"):
            add_word(word, plural, gender, translation_en, translation_zh, difficulty)

if __name__ == "__main__":
    main()