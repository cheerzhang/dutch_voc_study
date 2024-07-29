import streamlit as st
import pandas as pd
import os


def load_guest_data(data_type='NOUN'):
    if not os.path.exists("guest_NOUN.csv"):
        df = pd.DataFrame(columns=['word', 'plural', 'gender', 'translation_en', 'translation_zh', 'difficulty', 'search_count'])
        df.to_csv("guest_NOUN.csv", index=False)
    if not os.path.exists("guest_VERB.csv"):
        df = pd.DataFrame(columns=['verb', 'singular_present', 'plural_form', 'past_singular', 'past_plural', 'perfect_participle', 'translation_en', 'translation_zh', 'difficulty', 'search_count'])
        df.to_csv("guest_VERB.csv", index=False)
    df = pd.read_csv(f"guest_{data_type}.csv")
    return df

def load_user_data(username, data_type='NOUN'):
    guest_df = load_guest_data(data_type)
    if not os.path.exists(f"{username}_{data_type}.csv"):
        user_df = guest_df.copy()
        user_df['admin_search_count'] = 0
        user_df.to_csv(f"{username}_{data_type}.csv", index=False)
    user_df_ = pd.read_csv(f"{username}_{data_type}.csv")
    return guest_df, user_df_
    
    


