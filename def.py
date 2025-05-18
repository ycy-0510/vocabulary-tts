import google.generativeai as genai
import pandas as pd
import time

# 讀取 Excel
df = pd.read_excel("vocb.xlsx")
api_key = []
# 設定 Gemini API Key
genai.configure(api_key=api_key[0])
model = genai.GenerativeModel("gemini-2.0-flash-lite")

# 處理每個單字
example_ens = []
example_zhs = []

for index, row in df.iterrows():
    word = row['word']
    definition = row['pos_chinese']
    
    prompt = f"""
請為英文單字 "{word}"（意思是「{definition}」）寫一個簡單清楚的英文例句，並翻譯成中文。
請只回傳：
英文：...
中文：...
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # 簡單格式處理
        if "英文：" in text and "中文：" in text:
            en_line = text.split("英文：")[1].split("中文：")[0].strip()
            zh_line = text.split("中文：")[1].strip()
        else:
            en_line = ""
            zh_line = ""
        print(f"✅ 成功 {word}: {en_line} / {zh_line}")

    except Exception as e:
        print(f"⚠️ 失敗 {word}: {e}")
        en_line = ""
        zh_line = ""

    example_ens.append(en_line)
    example_zhs.append(zh_line)
    
    time.sleep(1.2)  # 避免請求過快造成 API 限制

# 加入新欄位
df['example_en'] = example_ens
df['example_zh'] = example_zhs

# 匯出新檔案
df.to_excel("含例句單字表.xlsx", index=False)
print("✅ 產生完成，已儲存為：含例句單字表.xlsx")