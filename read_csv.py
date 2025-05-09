import pandas as pd

import os
import glob
from zipfile import ZipFile


def read_multiple_csv(directory_path):
    all_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    df_list = []
    
    for file in all_files:
        file_path = os.path.join(directory_path, file)
        df = pd.read_csv(file_path)
        df_list.append(df)
    
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df
