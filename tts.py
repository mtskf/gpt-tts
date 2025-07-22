import openai
import os
import sys
import tiktoken
import re
from pathlib import Path
from dotenv import load_dotenv
import subprocess

# --- Configuration ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini-tts"
VOICE = "nova"
INSTRUCTIONS = (
    "Speak in a warm, clear, engaging, and expressive tone suitable for educational narration in both Japanese and English. "
    "Use natural pacing with gentle variation in pitch and emphasis to maintain attention and enhance learning. "
    "Add subtle pauses and rhythm to ensure the content is easy to follow and understand. "
    "Your delivery should feel thoughtful, confident, and human—like a friendly tutor guiding someone through important ideas."
)
RESPONSE_FORMAT = "mp3"
TOKEN_LIMIT = 2000

enc = tiktoken.get_encoding("cl100k_base")

def split_text_by_token(text):
    parts = []
    current = ""
    for sentence in re.split(r'(?<=[。．！？\n])', text):
        if not sentence.strip():
            continue
        tokens = enc.encode(current + sentence)
        if len(tokens) > TOKEN_LIMIT:
            parts.append(current.strip())
            current = sentence
        else:
            current += sentence
    if current.strip():
        parts.append(current.strip())
    return parts

def synthesize(text, index, prefix):
    print(f"🎙️ Generating Part {index + 1}...")
    response = openai.audio.speech.create(
        model=MODEL,
        voice=VOICE,
        input=text,
        instructions=INSTRUCTIONS,
        response_format=RESPONSE_FORMAT,
    )
    part_path = f"{prefix}_part{index + 1}.mp3"
    with open(part_path, "wb") as f:
        f.write(response.content)
    print(f"✅ Saved: {part_path}")
    return part_path

def merge_audio(parts, output_path):
    list_file = "concat_list.txt"
    with open(list_file, "w") as f:
        for part_path in parts:
            f.write(f"file '{part_path}'\n")
    print("🔄 Merging audio segments...")
    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file,
        "-c", "copy", output_path
    ], check=True)
    os.remove(list_file)
    print(f"🎧 Merged file created: {output_path}")

def main(input_file):
    input_path = Path(input_file)
    if not input_path.exists():
        print("❌ Input file not found.")
        sys.exit(1)

    with input_path.open("r", encoding="utf-8") as f:
        text = f.read().strip()

    print("✂️ Splitting text based on token length...")
    parts = split_text_by_token(text)
    print(f"📚 Number of segments: {len(parts)}")

    prefix = input_path.stem
    output_parts = []
    for i, part_text in enumerate(parts):
        print(f"🧮 Part {i+1} Character count: {len(part_text)} / Token count: {len(enc.encode(part_text))}")
        output_parts.append(synthesize(part_text, i, prefix))

    merged_file = f"{prefix}_merged.mp3"
    merge_audio(output_parts, merged_file)

    # Remove individual segment files
    for part_path in output_parts:
        try:
            os.remove(part_path)
            print(f"🗑️ Deleted: {part_path}")
        except Exception as e:
            print(f"⚠️ Failed to delete: {part_path} ({e})")
    print("✅ All done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tts_token_split_merge.py input.txt")
        sys.exit(1)
    main(sys.argv[1])
