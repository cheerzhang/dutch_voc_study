import streamlit as st
import pandas as pd
import os



def load_data(username, role, data_type='NOUN'):
    if not os.path.exists("guest_NOUN.csv"):
        df = pd.DataFrame(columns=['word', 'plural', 'gender', 'translation_en', 'translation_zh', 'difficulty', 'search_count', 'admin_search_count'])
        df.to_csv("guest_NOUN.csv", index=False)
    if not os.path.exists("guest_VERB.csv"):
        df = pd.DataFrame(columns=['verb', 'singular_present', 'plural_form', 'past_singular', 'past_plural', 'perfect_participle', 'translation_en', 'translation_zh', 'difficulty', 'search_count'])
        df.to_csv("guest_VERB.csv", index=False)
    if role == 'guest':
        df = pd.read_csv(f"guest_{data_type}.csv")
    elif role == 'admin':
        if not os.path.exists(f"{username}_{data_type}.csv"):
            df = pd.read_csv(f"guest_{data_type}.csv")
            df['admin_search_count'] = 0
        else:
            df_guest = pd.read_csv(f"guest_{data_type}.csv")
            df_user = pd.read_csv(f"{username}_{data_type}.csv")
            if data_type=='NOUN':
                df = df_guest.merge(
                    df_user[['word', 'admin_search_count']], 
                    on='word', 
                    how='left', 
                    suffixes=('', '_y')
                )  #.drop(columns=['admin_search_count_y'])
            if data_type=='VERB':
                df = df_guest.merge(
                    df_user[['verb', 'admin_search_count']], 
                    on='verb', 
                    how='left', 
                    suffixes=('', '_y')
                )
            df['admin_search_count'].fillna(0, inplace=True)
    return df

