import pandas as pd
import json
import os

# 匯入 Excel 檔案
input_file = "def.xlsx"
df = pd.read_excel(input_file)

# 加入原始順序欄位（從 1 開始）
df["idx"] = df.index + 1

# 正規化欄位名稱
df.columns = [col.strip().lower() for col in df.columns]

# 檢查必要欄位
required_columns = {"word", "pos_chinese", "level", "example_en", "example_zh", "kk"}
if not required_columns.issubset(set(df.columns)):
    raise ValueError(f"缺少欄位：{required_columns - set(df.columns)}")

# 輸出資料夾
output_dir = "output_json"
os.makedirs(output_dir, exist_ok=True)

# 每個 level 處理一次
for level in range(1, 7):
    level_df = df[df["level"] == level].copy()
    level_df = level_df.sort_values("word", key=lambda col: col.str.lower())  # 按照單字排序分組,不分大小寫 （a>A>b>B）

    sets = []
    current_set = []

    for row in level_df.itertuples(index=False):
        example = f"{row.example_en}\n{row.example_zh}"
        entry = {
            "term": row.word,
            "definition": row.pos_chinese,
            "example": example,
            "sound": row.idx,  # ← 使用原始 idx
            "kk": row.kk if pd.notna(row.kk) else "",  # 處理可能的 NaN
        }
        current_set.append(entry)

        if len(current_set) == 36:
            sets.append(current_set)
            current_set = []

    if current_set:
        sets.append(current_set)

    # 儲存 JSON
    output_path = os.path.join(output_dir, f"level-{level}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sets, f, ensure_ascii=False, indent=2)

    print(f"✅ 已輸出：{output_path}")