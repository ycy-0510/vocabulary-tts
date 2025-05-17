import os
import time
import pandas as pd
from google.cloud import texttospeech
from zipfile import ZipFile

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tts.json"
client = texttospeech.TextToSpeechClient()

df = pd.read_excel("vocb.xlsx") #|words|pos_chinese|level|

output_dir = "audio_files"
os.makedirs(output_dir, exist_ok=True)

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

k=1
for i, row in df.iterrows():
    word = row["word"]
    synthesis_input = texttospeech.SynthesisInput(text=word)

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    filename = os.path.join(output_dir, f"{k}.mp3")
    with open(filename, "wb") as out:
        out.write(response.audio_content)
    print(f"已儲存: {filename}")
    k += 1
    # delay () (rate 800 char per minute)
    time.sleep(0.1) 


# --- 壓縮成 zip ---
zip_name = "word_audio_files.zip"
with ZipFile(zip_name, "w") as zipf:
    for file in os.listdir(output_dir):
        zipf.write(os.path.join(output_dir, file), arcname=file)

print(f"\n所有音檔已壓縮為：{zip_name}")