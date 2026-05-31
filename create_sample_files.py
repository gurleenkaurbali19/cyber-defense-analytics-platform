import pandas as pd
import os

DATA_FOLDER = "Data"
OUTPUT_FOLDER = "Data/SampleFiles"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

files = {
    "falcon": "falcon_jan.xlsx",
    "cyble": "cyble_jan.xlsx",
    "siem": "siem_jan.xlsx",
    "trend": "trend_jan.xlsx",
    "netskope": "netskope_jan.xlsx",
    "comolho": "comolho_jan.xlsx"
}

for tool, filename in files.items():

    path = os.path.join(DATA_FOLDER, filename)

    df = pd.read_excel(path)

    sample_df = df.sample(
        n=min(15, len(df)),
        random_state=42
    )

    sample_path = os.path.join(
        OUTPUT_FOLDER,
        f"{tool}_sample.xlsx"
    )

    sample_df.to_excel(
        sample_path,
        index=False
    )

print("Sample files created")