import os
import pandas as pd

DEFAULT_COLUMNS = {
    'noun': ['word', 'plural', 'gender', 'translation_en', 'translation_zh', 'difficulty', 'search_count'],
    'verb': ['verb', 'singular_present', 'plural_form', 'past_singular', 'past_plural', 'perfect_participle', 'translation_en', 'translation_zh', 'difficulty', 'search_count']
}

def load_or_create_csv(file_path, data_type):
    columns = DEFAULT_COLUMNS.get(data_type, [])
    if not columns:
        raise ValueError(f"Unknown data_type: {data_type}")
    
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        return df

def save_csv(df, file_path):
    df.to_csv(file_path, index=False)
