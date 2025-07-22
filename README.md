# GPT-4o Text-to-Speech (TTS) Tool

This Python script converts long text files into high-quality MP3 audio using OpenAI's `gpt-4o-mini-tts` model. It automatically splits the input text based on token limits, synthesizes audio for each segment, and merges the segments into one seamless output file.

## Features

- Supports large text inputs by splitting them into token-safe segments
- Uses expressive narration suitable for educational purposes
- Automatically merges audio segments using `ffmpeg`
- Clean-up of temporary files after merging

## Requirements

- Python 3.8+
- ffmpeg (must be installed and accessible via command line)
- OpenAI API key

Install dependencies:

```bash
pip install openai python-dotenv tiktoken
```

## Usage

```bash
python tts.py your_text_file.txt
```

Example:

```bash
python tts.py article.txt
```

This will generate:

- `article_part1.mp3`, `article_part2.mp3`, ...
- `article_merged.mp3` — the final merged output

## Environment Variables

Create a `.env` file with the following content:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Notes

- The voice used is `nova` (you can change it in the script).
- The tone is designed for clear, friendly, and expressive narration.

## License

MIT License
