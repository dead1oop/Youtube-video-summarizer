"""Demo: extract transcript + generate summary (same flow as the app)."""

from modules.env_loader import load_env
from modules.transcript import TranscriptExtractor
from modules.summarizer import Summarizer

load_env()

# Short educational video with reliable English captions
URL = "https://www.youtube.com/watch?v=aircAruvnKk"

print("=" * 60)
print("SmartTube AI — Live Demo")
print("=" * 60)
print(f"\nVideo URL: {URL}\n")

print("[1/2] Extracting transcript...")
result = TranscriptExtractor().extract(URL, "en")

if not result["success"]:
    print(f"FAILED: {result['error']}")
    raise SystemExit(1)

print(f"  Title:    {result['title']}")
print(f"  Words:    {result['word_count']}")
print(f"  Language: {result['language']}")
print(f"  Preview:  {result['transcript'][:200]}...\n")

print("[2/2] Generating summary...")
summary = Summarizer().summarize(result["transcript"], "concise")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(summary)
print("\n" + "=" * 60)
print("Done! Open http://localhost:8501 to use the web app.")
print("=" * 60)
