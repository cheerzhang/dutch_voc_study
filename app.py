import streamlit as st
import pandas as pd
import sqlite3

# 连接数据库
def get_connection():
    conn = sqlite3.connect('dutch_words.db')
    return conn

# 获取所有单词
def get_words():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words ORDER BY search_count DESC")
    words = cursor.fetchall()
    conn.close()
    return words

# 添加新单词
def add_word_to_db(word, plural, gender, translation_en, translation_zh, difficulty):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO words (word, plural, gender, translation_en, translation_zh, difficulty)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (word, plural, gender, translation_en, translation_zh, difficulty))
    conn.commit()
    conn.close()

# 搜索单词
def search_word_from_db(word):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words WHERE word=?", (word,))
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE words SET search_count = search_count + 1 WHERE id=?", (result[0],))
        conn.commit()
    conn.close()
    return result

# Streamlit 应用
st.title('Dutch Words Learning Tool')

# 添加单词
st.header('Add a New Word')
with st.expander("Add a New Word"):
    with st.form(key='add_word_form'):
        word = st.text_input('Word')
        plural = st.text_input('Plural')
        gender = st.selectbox('Gender', ['de', 'het'])
        translation_en = st.text_input('English Translation')
        translation_zh = st.text_input('Chinese Translation')
        difficulty = st.selectbox('Difficulty', ['A1', 'A2', 'B1', 'B2', 'C1'])
        submit_add = st.form_submit_button('Add Word')

        if submit_add and word and plural and translation_en and translation_zh:
            add_word_to_db(word, plural, gender, translation_en, translation_zh, difficulty)
            st.success(f'Word "{word}" added to the database.')

# 搜索单词
st.header('Search for a Word')
with st.form(key='search_word_form'):
    search_word = st.text_input('Enter the Dutch word to search')
    submit_search = st.form_submit_button('Search')

    if submit_search and search_word:
        result = search_word_from_db(search_word)
        if result:
            st.write(f"**Word:** {result[1]}")
            st.write(f"**Plural:** {result[2]}")
            st.write(f"**Gender:** {result[3]}")
            st.write(f"**English Translation:** {result[4]}")
            st.write(f"**Chinese Translation:** {result[5]}")
            st.write(f"**Difficulty:** {result[6]}")
            st.write(f"**Search Count:** {result[7]}")
        else:
            st.error(f'Word "{search_word}" not found in the database.')

# 显示所有单词
st.header('All Words in the Database')
words = get_words()

# 将数据转换为Pandas DataFrame
df = pd.DataFrame(words, columns=['ID', 'Word', 'Plural', 'Gender', 'English Translation', 'Chinese Translation', 'Difficulty', 'Search Count'])

if not df.empty:
    # 使用st.dataframe显示DataFrame
    st.dataframe(df.drop(columns=['ID']), width=800, height=400)
else:
    st.write('No words in the database.')