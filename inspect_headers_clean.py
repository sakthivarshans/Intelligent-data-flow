
import pandas as pd
import glob
import os

def inspect_file(pattern):
    print(f"--- Inspecting pattern: {pattern} ---")
    files = glob.glob(pattern)
    if not files:
        print("No files found.")
        return
    
    f = files[0]
    print(f"File: {os.path.basename(f)}")
    try:
        df = pd.read_excel(f, nrows=2)
        print("Columns:")
        for c in df.columns:
            print(f"  - {c}")
        print("First row:")
        print(df.iloc[0].to_dict())
    except Exception as e:
        print(f"Error: {e}")

inspect_file("data/raw/train/Study_04/*Visit Projection*.xlsx")
inspect_file("data/raw/train/Study_04/*Missing*Page*.xlsx")
