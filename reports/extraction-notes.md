# Extraction Notes & Summary Report

This document records the extraction process, per-week question counts, answer-key formats, figure extractions, and notes on ambiguities across Weeks 1 to 11.

---

## Overall Summary

- **Total Weeks:** 11 (Week 1 through Week 11)
- **Total Questions:** 110 (10 questions per week)
- **Validation Status:** `scripts/validate.py` passed with 0 errors across all 11 weeks.
- **Data Bundle:** `data/quiz-data.js` compiled with `window.QUIZ_DATA` mapping keys `"1"` to `"11"`.
- **Zero Explanations/Hints:** All explanation and solution texts from the source PDFs have been completely excluded in adherence to strict constraints.

---

## Per-Week Breakdown

### Week 01 (`assets/1.pdf`)
- **Question Count:** 10 questions.
- **Answer-Key Format:** Explicit `Correct answer: (x) ...` inline lines beneath each question and marked bullet `▸` with green text (`#1b7a3d`).
- **Figures Extracted:** 1 figure (`assets/figures/week01/q005-fig1.png` - Git file lifecycle state diagram for Q5).
- **Notes / Observations:**
  - Q2 is multi-answer: (a), (b), (c) are all correct.
  - Q8 is multi-answer: (a), (b), (c), (d) are all correct.
  - Q10 options are labelled `(A)` through `(D)` in uppercase in the PDF.

### Week 02 (`assets/2.docx.pdf`)
- **Question Count:** 10 questions.
- **Answer-Key Format:** Correct options formatted in red color (`0xff0000`) within the option lines.
- **Figures Extracted:** 0 figures (all questions and options are pure text and code).
- **Notes / Observations:**
  - Q5 is multi-answer: options (b) and (d) are both highlighted in red ("Presence of negative emotion words" and "Presence of pronouns").

### Week 03 (`assets/3.docx.pdf`)
- **Question Count:** 10 questions.
- **Answer-Key Format:** Correct options formatted in red text (`0xff0000`), corroborated by inline worked solutions (e.g., Q4 NDCG calculation).
- **Figures Extracted:** 1 figure (`assets/figures/week03/q008-fig1.png` - CDF graph for Q8).
- **Notes / Observations:**
  - Q2 is multi-answer: all four options (a, b, c, d) are highlighted in red ("Tweet links", "Tweet Author", "Tweet network", "Tweet meta data").

### Week 04 (`assets/4.docx.pdf`)
- **Question Count:** 10 questions.
- **Answer-Key Format:** Correct options formatted in red text (`0xff0000`) and confirmed by the `Solutions` section on pages 5-6.
- **Figures Extracted:** 3 figure crops (`assets/figures/week04/q008-optA.png`, `q008-optB.png`, `q008-optC.png` for Q8 table options).
- **Notes / Observations:**
  - Q8 options A, B, C are tables generated from Pandas `groupby`. Option D ("None of the above") is the correct answer in red. Both clean text representations and high-resolution table image crops are provided.

### Week 05 (`assets/5.docx.pdf`)
- **Question Count:** 10 questions.
- **Answer-Key Format:** Correct options highlighted in red text (`0xff0000`), corroborated by the `Solutions:` section on page 4.
- **Figures Extracted:** 2 figures (`assets/figures/week05/q003-fig1.png` for Q3 and `assets/figures/week05/q004-fig1.png` for Q4).
- **Notes / Observations:**
  - Q1 is multi-answer: all 4 options (a, b, c, d) are highlighted in red.
  - Q2 is multi-answer: options (a) and (b) are highlighted in red.

### Week 06 (`assets/6.pdf`)
- **Question Count:** 10 questions.
- **Answer-Key Format:** Dedicated Answer Key table on page 6, plus inline `Answer:` lines, checkmarks `✔`, and green bold styling (`#1b7f3b`) on correct options.
- **Figures Extracted:** 1 figure (`assets/figures/week06/q010-fig1.png` - link farming diagram for Q10).
- **Notes / Observations:**
  - Multi-answer questions: Q5 (`["A", "B"]`), Q9 (`["A", "B", "C", "D"]`), Q10 (`["A", "B"]`).
  - NPTEL banner watermark logo present on all pages was identified and excluded from question figures.

### Week 07 (`assets/7.pdf`)
- **Question Count:** 10 questions.
- **Answer-Key Format:** Dedicated Answer Key table on pages 6-7, plus inline `Answer:` lines and checkmarks `✔`.
- **Figures Extracted:** 2 figures (`assets/figures/week07/q004-fig1.png` - sample phishing email for Q4, and `assets/figures/week07/q008-fig1.png` - audience picture nudge for Q8).
- **Notes / Observations:**
  - Q1 options are labelled `Option (a)` to `Option (d)` with Python code strings.
  - Single-answer questions across the entire week.

### Week 08 (`assets/8.pdf`)
- **Question Count:** 10 questions.
- **Answer-Key Format:** Dedicated Answer Key table on page 6, plus inline `Answer:` lines and checkmarks `✔`.
- **Figures Extracted:** 1 figure (`assets/figures/week08/q003-fig1.png` - username and profile attribute change CDF bar graph for Q3).
- **Notes / Observations:**
  - Multi-answer questions: Q1 (`["A", "B"]`), Q6 (`["A", "B", "C", "D"]`), Q8 (`["A", "B", "C", "D"]`).

### Week 09 (`assets/9.pdf`)
- **Question Count:** 10 questions.
- **Answer-Key Format:** Dedicated Answer Key table spanning pages 6-7, plus inline `Answer:` lines and checkmarks `✔`.
- **Figures Extracted:** 3 figures (`assets/figures/week09/q005-fig1.png` for Q5 Figure 2, `assets/figures/week09/q008-fig1.png` for Q8 bubble plot, `assets/figures/week09/q010-fig1.png` for Q10 Figure 4 & 5).
- **Notes / Observations:**
  - Multi-answer questions: Q1 (`["A", "B", "C", "D"]`), Q4 (`["A", "C"]`), Q6 (`["A", "B"]`), Q7 (`["A", "B", "C"]`), Q10 (`["A", "B", "C", "D"]`).

### Week 10 (`assets/10.pdf`)
- **Question Count:** 10 questions.
- **Answer-Key Format:** Dedicated Answer Key table on page 6, plus inline `Answer:` lines and checkmarks `✔`.
- **Figures Extracted:** 4 figures (`assets/figures/week10/q003-fig1.png` for Q3 UGI quality, `assets/figures/week10/q005-fig1.png` for Q5 username dynamics CDF, `assets/figures/week10/q008-fig1.png` for Q8 Boston blast fake tweets, `assets/figures/week10/q010-fig1.png` for Q10 temporal distribution plot).
- **Notes / Observations:**
  - Multi-answer questions: Q1 (`["A", "B", "C"]`), Q3 (`["A", "D"]`), Q9 (`["A", "B", "C"]`).

### Week 11 (`assets/11.pdf`)
- **Question Count:** 10 questions.
- **Answer-Key Format:** Dedicated Answer Key table on page 5, plus inline `Answer:` lines and checkmarks `✔`.
- **Figures Extracted:** 0 figures (all questions and options are pure text).
- **Notes / Observations:**
  - Multi-answer questions: Q2 (`["A", "D"]`), Q3 (`["A", "B", "C", "D"]`), Q4 (`["A", "C"]`), Q5 (`["B", "D"]`).

---

## Uncertainties / Items to Flag
- **No Unresolved Missing Answers:** Every question across all 11 weeks has an unambiguous, PDF-stated answer matching both marked options and answer keys.
- **No Solutions/Explanations in App Data:** Verified that all JSON files contain exclusively question text, option texts/images, answer option ids, and metadata.
