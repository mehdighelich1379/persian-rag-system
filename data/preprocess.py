import json
from pathlib import Path

# ===============================
# Paths
# ===============================
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "generated_dataset.jsonl"
OUTPUT_FILE = BASE_DIR / "fine_tune_FINAL.jsonl"
ERROR_LOG = BASE_DIR / "bad_chunks.log"

assert INPUT_FILE.exists(), "❌ Input dataset not found"
assert not OUTPUT_FILE.exists(), "❌ Output file already exists"

# ===============================
# Prompts
# ===============================
SYSTEM_PROMPT = (
    "You are a technical HR expert. "
    "You write professional, practical educational texts "
    "tailored to specific roles and categories."
)

# ===============================
# Helpers
# ===============================
def fix_text(text):
    if not isinstance(text, str):
        return ""
    try:
        return text.encode("latin1").decode("utf-8")
    except Exception:
        return text

def build_user_prompt(row):
    role = row.get("role")
    category = row.get("category")
    if role:
        return f"برای نقش {role} یک متن آموزشی حرفه‌ای بنویس."
    return f"یک متن آموزشی حرفه‌ای درباره {category} بنویس."

def flatten(obj):
    if isinstance(obj, dict):
        yield obj
    elif isinstance(obj, list):
        for item in obj:
            yield from flatten(item)

# ===============================
# Brutal but Safe JSON extractor
# ===============================
total = 0
bad = 0
buffer = ""

with INPUT_FILE.open("r", encoding="utf-8", errors="ignore") as fin, \
     OUTPUT_FILE.open("w", encoding="utf-8") as fout, \
     ERROR_LOG.open("w", encoding="utf-8") as log:

    for line_no, line in enumerate(fin, start=1):
        buffer += line.strip()

        try:
            data = json.loads(buffer)
            buffer = ""
        except json.JSONDecodeError:
            if len(buffer) > 20000:
                log.write(f"Skipped large broken chunk at line {line_no}\n")
                buffer = ""
                bad += 1
            continue

        for row in flatten(data):
            sample = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": fix_text(build_user_prompt(row))},
                    {"role": "assistant", "content": fix_text(row.get("text", "")).strip()}
                ]
            }
            fout.write(json.dumps(sample, ensure_ascii=False) + "\n")
            total += 1

print("✅ Preprocess finished successfully")
print(f"🟢 Total rows written: {total}")
print(f"🔴 Skipped broken chunks: {bad}")
print(f"📄 Output file: {OUTPUT_FILE}")
print(f"📝 Error log: {ERROR_LOG}")
