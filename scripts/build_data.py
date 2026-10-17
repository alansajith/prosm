"""
scripts/build_data.py
Merges all week files (data/week01.json ... week11.json) into data/quiz-data.js:
window.QUIZ_DATA = { "1": [ ... ], "2": [ ... ], ... "11": [ ... ] };
Works seamlessly offline and via file:// protocol.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "quiz-data.js")

def main():
    bundle = {}
    for w in range(1, 12):
        filename = f"week{w:02d}.json"
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Missing {filepath}")
            
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            bundle[str(w)] = data.get("questions", [])
            
    js_content = "/**\n * Auto-generated bundle of quiz questions for Weeks 1-11.\n * Do not edit directly. Run `python scripts/build_data.py` to rebuild.\n */\n"
    js_content += "window.QUIZ_DATA = " + json.dumps(bundle, indent=2, ensure_ascii=False) + ";\n"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"Successfully generated {OUTPUT_FILE} with {len(bundle)} weeks ({sum(len(q) for q in bundle.values())} total questions).")

if __name__ == "__main__":
    main()
