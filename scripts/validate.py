"""
scripts/validate.py
Sanity checks for extracted MCQ data per Section 5.6 of AGENTS.md:
- Question numbers are sequential with no gaps or duplicates.
- Every question has at least 2 options, and every option has text or an image.
- Every question has a non-empty answer whose ids all exist in options.
- Every referenced image file exists.
- Total count per week matches what the PDF shows (10 per week, 110 total).
- No JSON field contains an explanation or hint.
"""

import os
import json
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

FORBIDDEN_KEYS = ["explanation", "hint", "rationale", "solution", "solution_text", "notes"]

def validate_week(week_num):
    filename = f"week{week_num:02d}.json"
    filepath = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        return [f"File {filename} does not exist."]
    
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            return [f"Failed to parse JSON {filename}: {e}"]
            
    errors = []
    
    # Check week number and source_pdf
    if data.get("week") != week_num:
        errors.append(f"Expected week {week_num}, got {data.get('week')}")
        
    source_pdf = data.get("source_pdf")
    if not source_pdf or not os.path.exists(os.path.join(BASE_DIR, source_pdf)):
        errors.append(f"Source PDF does not exist: {source_pdf}")
        
    questions = data.get("questions", [])
    if len(questions) != 10:
        errors.append(f"Expected 10 questions in week {week_num}, got {len(questions)}")
        
    seen_numbers = set()
    
    for i, q in enumerate(questions):
        q_id = q.get("id", f"index-{i}")
        q_num = q.get("number")
        
        # Check forbidden explanation/hint keys
        for key in q.keys():
            if key.lower() in FORBIDDEN_KEYS:
                errors.append(f"[{q_id}] Forbidden key found: {key}")
                
        # Check sequential numbering
        if q_num != i + 1:
            errors.append(f"[{q_id}] Question number {q_num} is not sequential (expected {i + 1})")
        if q_num in seen_numbers:
            errors.append(f"[{q_id}] Duplicate question number {q_num}")
        seen_numbers.add(q_num)
        
        # Check type
        q_type = q.get("type")
        if q_type not in ["single", "multi"]:
            errors.append(f"[{q_id}] Invalid type: {q_type}")
            
        # Check question structure
        question_obj = q.get("question", {})
        q_text = question_obj.get("text", "")
        q_images = question_obj.get("images", [])
        
        if not q_text and not q_images:
            errors.append(f"[{q_id}] Question has neither text nor images")
            
        for img in q_images:
            img_path = os.path.join(BASE_DIR, img)
            if not os.path.exists(img_path):
                errors.append(f"[{q_id}] Referenced question image does not exist: {img}")
                
        # Check options
        options = q.get("options", [])
        if len(options) < 2:
            errors.append(f"[{q_id}] Expected at least 2 options, got {len(options)}")
            
        option_ids = set()
        for opt in options:
            opt_id = opt.get("id")
            opt_text = opt.get("text", "")
            opt_img = opt.get("image")
            
            if not opt_id:
                errors.append(f"[{q_id}] Option missing id")
            if opt_id in option_ids:
                errors.append(f"[{q_id}] Duplicate option id: {opt_id}")
            option_ids.add(opt_id)
            
            if not opt_text and not opt_img:
                errors.append(f"[{q_id}] Option {opt_id} has neither text nor image")
                
            if opt_img:
                opt_img_path = os.path.join(BASE_DIR, opt_img)
                if not os.path.exists(opt_img_path):
                    errors.append(f"[{q_id}] Referenced option image does not exist: {opt_img}")
                    
        # Check answer
        answers = q.get("answer", [])
        if not isinstance(answers, list) or len(answers) == 0:
            errors.append(f"[{q_id}] Answer must be a non-empty list, got {answers}")
        else:
            for ans in answers:
                if ans not in option_ids:
                    errors.append(f"[{q_id}] Answer id '{ans}' not found in option ids: {option_ids}")
                    
            if q_type == "single" and len(answers) > 1:
                errors.append(f"[{q_id}] Type is 'single' but answer has multiple items: {answers}")
                
        # Check source
        source = q.get("source", {})
        if not source.get("page"):
            errors.append(f"[{q_id}] Missing source page")
            
    return errors


def main():
    total_errors = 0
    total_questions = 0
    print("=" * 60)
    print("RUNNING MCQ DATA VALIDATION")
    print("=" * 60)
    
    for w in range(1, 12):
        errs = validate_week(w)
        if errs:
            print(f"FAILED: Week {w} has {len(errs)} error(s):")
            for err in errs:
                print(f"  - {err}")
            total_errors += len(errs)
        else:
            print(f"PASSED: Week {w:02d} (10 questions, all checks passed)")
            total_questions += 10
            
    print("=" * 60)
    if total_errors == 0:
        print(f"ALL CHECKS PASSED WITH ZERO ERRORS! (Total questions: {total_questions})")
        return 0
    else:
        print(f"VALIDATION FAILED WITH {total_errors} TOTAL ERROR(S)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
