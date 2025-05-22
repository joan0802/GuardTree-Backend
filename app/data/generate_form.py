import pandas as pd
import json

meta_path = "app/data/form_metadata.csv"
df_meta = pd.read_csv(meta_path, skiprows=1, sep=None, engine="python")
df_meta.columns = ["source_form", "core_area", "activity", "item", "subitem"]

forms_data = {}

for form in sorted(df_meta["source_form"].unique()):
    form_df = df_meta[df_meta["source_form"] == form]
    form_records = []
    for _, row in form_df.iterrows():
        entry = {
            "activity": row["activity"],
            "item": row["item"],
            "subitem": row["subitem"] if not pd.isna(row["subitem"]) else None,
            "core_area": row["core_area"],
            "support_type": None
        }
        form_records.append(entry)
    forms_data[f"form_{form}"] = form_records

output_path = "app/data/form.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(forms_data, f, ensure_ascii=False, indent=2)

output_path
