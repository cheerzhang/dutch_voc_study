import streamlit as st
import pandas as pd
import os


def load_guest_data(data_type='NOUN'):
    df = pd.read_csv(f"guest_{data_type}.csv")
    return df

def load_user_data(username, data_type='NOUN'):
    guest_df = load_guest_data(data_type)
    if not os.path.exists(f"{username}_{data_type}.csv"):
        user_df = guest_df.copy()
        user_df['admin_search_count'] = 0
        user_df.to_csv(f"{username}_{data_type}.csv", index=False)
    else:
        user_df = pd.read_csv(f"{username}_{data_type}.csv")
    return guest_df, user_df
    
    


