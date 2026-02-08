
import pandas as pd
import glob
import os

with open("columns_dump.txt", "w") as out:
    def dump_cols(pattern):
        out.write(f"\n--- Pattern: {pattern} ---\n")
        files = glob.glob(pattern)
        if not files:
            out.write("No files found.\n")
            return
        f = files[0]
        out.write(f"File: {os.path.basename(f)}\n")
        try:
            df = pd.read_excel(f, nrows=2)
            out.write(f"Columns: {list(df.columns)}\n")
            out.write(f"First Row: {df.iloc[0].to_dict()}\n")
        except Exception as e:
            out.write(f"Error: {e}\n")

    dump_cols("data/raw/train/Study_04/*Visit Projection*.xlsx")
    dump_cols("data/raw/train/Study_04/*Missing*Page*.xlsx")
