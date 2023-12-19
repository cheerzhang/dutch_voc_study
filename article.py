import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import text


def search_dutch_list(dutch_arr):
    dutch_values_str = ', '.join([f"'{value}'" for value in dutch_arr])
    sql = f"SELECT * FROM dutch_vocabulary WHERE dutch in ({dutch_values_str});"
    try:
        df = conn.query(sql)
        return df
    except Exception as e:
        st.error(f"Error executing search query: {e}")


def search_data(dutch):
    sql = f"SELECT * FROM dutch_vocabulary WHERE dutch = '{dutch}';"
    try:
        df = conn.query(sql)
        st.write(df.shape)
        if df.shape[0] > 0:
            st.dataframe(df)
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error executing search query: {e}")



def insert_data(dutch, english):
    sql = text("INSERT INTO dutch_vocabulary (dutch, english, date) VALUES (:n1, :n2, CURRENT_DATE);")
    try:
        with conn.session as session:
            session.execute(sql, {'n1':dutch, 'n2': english})
            session.commit()
            st.success("Data inserted successfully!")
    except Exception as e:
        st.error(f"Error inserting data: {e}")



def get_article_voc():
    txt = st.text_area(
        "Article to learn",
        "", 
        height = 500
    )
    txt = txt.replace('.', ' ').replace('\n', '')
    voc_arr = txt.split(' ')
    return voc_arr



def add_voc_func(voc_arr):
    col_voc, col_trans = st.columns(2)
    with col_voc:
        option_voc = st.selectbox(
            'New word',
            voc_arr
        )
    with col_trans:
        voc_translate = st.text_input('Translate', '')
    if st.button("Add"):
        if option_voc is '' or voc_translate is '':
            st.write("fill in voc and translation")
        else:
            result = search_data(option_voc)
            if result is False:
                insert_data(option_voc, voc_translate)
                st.write("Added")
            else:
                st.write("Already existed.")
    else:
        st.write("fill in voc and translation, and then click Add")
            



conn = st.connection("postgresql", type="sql")
page_title = f'Article'
page_add_voc = f'Add word'
page_other = f'Other'
new_df = []
tab_article, tab_add_voc, tab_other = st.tabs([page_title, page_add_voc, page_other])
with tab_article:
    st.title(page_title)
    col_article, col_voc = st.columns([3, 1])
    with col_article:
        voc_arr = get_article_voc()
    with col_voc:
        voc_set = list(set(voc_arr))
        if '' in voc_set:
            voc_set.remove('')
        if len(voc_set) > 1:
            existed_df = search_dutch_list(voc_set)
        new_df = [item for item in voc_set if item not in existed_df.values]
        if len(new_df) > 0:
            st.dataframe(new_df, use_container_width=True)
        else:
            st.markdown("#### There is no new word.")
        # st.dataframe(voc_set, use_container_width=True)
with tab_add_voc:
    st.title(page_add_voc)
    add_voc_func(new_df)

    