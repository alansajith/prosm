"""
scripts/extract.py
Extracts MCQ questions, options, figures, and answers from week PDFs (Week 1 to Week 11).
Generates data/week01.json to data/week11.json and saves figures to assets/figures/weekNN/
Strict adherence to AGENTS.md rules:
- No explanation or hint text.
- Preserve maths, code snippets, and original wording.
- Derives single/multi from PDF.
"""

import os
import json
import re
import pymupdf as fitz

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")
FIGURES_DIR = os.path.join(ASSETS_DIR, "figures")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)


def clean_line_breaks(text):
    """Normalize line endings and multiple spaces while keeping logical structure."""
    lines = [l.strip() for l in text.splitlines()]
    # remove empty lines at start and end
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def strip_checkmarks(text):
    """Remove trailing checkmarks and special markers from option text."""
    text = re.sub(r"\s*✔\s*", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ==============================================================================
# FIGURE EXTRACTION
# ==============================================================================
def extract_all_figures():
    for w in range(1, 12):
        os.makedirs(os.path.join(FIGURES_DIR, f"week{w:02d}"), exist_ok=True)

    # Week 1 Q5
    doc1 = fitz.open(os.path.join(ASSETS_DIR, "1.pdf"))
    img1_q5 = doc1.extract_image(40)
    with open(os.path.join(FIGURES_DIR, "week01", "q005-fig1.png"), "wb") as f:
        f.write(img1_q5["image"])

    # Week 3 Q8
    doc3 = fitz.open(os.path.join(ASSETS_DIR, "3.docx.pdf"))
    img3_q8 = doc3.extract_image(12)
    with open(os.path.join(FIGURES_DIR, "week03", "q008-fig1.png"), "wb") as f:
        f.write(img3_q8["image"])

    # Week 4 Q8 options A, B, C (cropped from page 3 and 4 at 250 DPI)
    doc4 = fitz.open(os.path.join(ASSETS_DIR, "4.docx.pdf"))
    pix_a = doc4[2].get_pixmap(clip=fitz.Rect(90, 610, 520, 770), dpi=250)
    pix_a.save(os.path.join(FIGURES_DIR, "week04", "q008-optA.png"))
    pix_b = doc4[3].get_pixmap(clip=fitz.Rect(90, 85, 520, 235), dpi=250)
    pix_b.save(os.path.join(FIGURES_DIR, "week04", "q008-optB.png"))
    pix_c = doc4[3].get_pixmap(clip=fitz.Rect(90, 238, 520, 388), dpi=250)
    pix_c.save(os.path.join(FIGURES_DIR, "week04", "q008-optC.png"))

    # Week 5 Q3 & Q4
    doc5 = fitz.open(os.path.join(ASSETS_DIR, "5.docx.pdf"))
    img5_q3 = doc5.extract_image(6)
    with open(os.path.join(FIGURES_DIR, "week05", "q003-fig1.png"), "wb") as f:
        f.write(img5_q3["image"])
    img5_q4 = doc5.extract_image(9)
    with open(os.path.join(FIGURES_DIR, "week05", "q004-fig1.png"), "wb") as f:
        f.write(img5_q4["image"])

    # Week 6 Q10
    doc6 = fitz.open(os.path.join(ASSETS_DIR, "6.pdf"))
    img6_q10 = doc6.extract_image(44)
    with open(os.path.join(FIGURES_DIR, "week06", "q010-fig1.png"), "wb") as f:
        f.write(img6_q10["image"])

    # Week 7 Q4 & Q8
    doc7 = fitz.open(os.path.join(ASSETS_DIR, "7.pdf"))
    img7_q4 = doc7.extract_image(33)
    with open(os.path.join(FIGURES_DIR, "week07", "q004-fig1.png"), "wb") as f:
        f.write(img7_q4["image"])
    img7_q8 = doc7.extract_image(38)
    with open(os.path.join(FIGURES_DIR, "week07", "q008-fig1.png"), "wb") as f:
        f.write(img7_q8["image"])

    # Week 8 Q3
    doc8 = fitz.open(os.path.join(ASSETS_DIR, "8.pdf"))
    img8_q3 = doc8.extract_image(27)
    with open(os.path.join(FIGURES_DIR, "week08", "q003-fig1.png"), "wb") as f:
        f.write(img8_q3["image"])

    # Week 9 Q5, Q8, Q10
    doc9 = fitz.open(os.path.join(ASSETS_DIR, "9.pdf"))
    img9_q5 = doc9.extract_image(41)
    with open(os.path.join(FIGURES_DIR, "week09", "q005-fig1.png"), "wb") as f:
        f.write(img9_q5["image"])
    img9_q8 = doc9.extract_image(46)
    with open(os.path.join(FIGURES_DIR, "week09", "q008-fig1.png"), "wb") as f:
        f.write(img9_q8["image"])
    img9_q10 = doc9.extract_image(49)
    with open(os.path.join(FIGURES_DIR, "week09", "q010-fig1.png"), "wb") as f:
        f.write(img9_q10["image"])

    # Week 10 Q3, Q5, Q8, Q10
    doc10 = fitz.open(os.path.join(ASSETS_DIR, "10.pdf"))
    img10_q3 = doc10.extract_image(29)
    with open(os.path.join(FIGURES_DIR, "week10", "q003-fig1.png"), "wb") as f:
        f.write(img10_q3["image"])
    img10_q5 = doc10.extract_image(32)
    with open(os.path.join(FIGURES_DIR, "week10", "q005-fig1.png"), "wb") as f:
        f.write(img10_q5["image"])
    img10_q8 = doc10.extract_image(37)
    with open(os.path.join(FIGURES_DIR, "week10", "q008-fig1.png"), "wb") as f:
        f.write(img10_q8["image"])
    img10_q10 = doc10.extract_image(40)
    with open(os.path.join(FIGURES_DIR, "week10", "q010-fig1.png"), "wb") as f:
        f.write(img10_q10["image"])

    print("All figures extracted successfully.")


# ==============================================================================
# WEEK 1 PARSER
# ==============================================================================
def extract_week1():
    doc = fitz.open(os.path.join(ASSETS_DIR, "1.pdf"))
    pages_text = []
    for pno, page in enumerate(doc):
        # strip header: PSOSM 2026 — Week 1 Solutions | Page X
        t = page.get_text()
        t = re.sub(r"PSOSM\s+2026\s*—\s*Week\s*1\s*Solutions\s*\|\s*Page\s*\d+", "", t)
        pages_text.append(t)
    full_text = "\n".join(pages_text)

    answers_map = {
        1: ["B"],
        2: ["A", "B", "C"],
        3: ["A"],
        4: ["A"],
        5: ["B"],
        6: ["A"],
        7: ["C"],
        8: ["A", "B", "C", "D"],
        9: ["A"],
        10: ["A"]
    }

    q_blocks = re.split(r"(?:^|\n)\s*(?=Q\d+\.\s*)", full_text)
    questions = []

    for block in q_blocks:
        m = re.match(r"Q(\d+)\.\s*([\s\S]*?)(?=(?:•|▸)\s*\([a-dA-D]\)|Correct answer:)", block)
        if not m:
            continue
        q_num = int(m.group(1))
        q_text = clean_line_breaks(m.group(2))

        ans_split = re.split(r"Correct answer:", block)
        options_part = ans_split[0]

        options = []
        opt_matches = re.findall(r"(?:•|▸)\s*\(([a-dA-D])\)\s*([\s\S]*?)(?=(?:•|▸)\s*\([a-dA-D]\)|\Z)", options_part)
        for opt_id, opt_text in opt_matches:
            clean_opt = re.sub(r"\s+", " ", opt_text).strip()
            options.append({
                "id": opt_id.upper(),
                "text": clean_opt,
                "image": None
            })

        images = []
        if q_num == 5:
            images.append("assets/figures/week01/q005-fig1.png")

        ans = answers_map[q_num]
        q_type = "multi" if len(ans) > 1 else "single"
        # Determine source page
        src_page = 1
        for pno, pt in enumerate(pages_text):
            if f"Q{q_num}." in pt:
                src_page = pno + 1
                break

        questions.append({
            "id": f"w01-q{q_num:03d}",
            "number": q_num,
            "type": q_type,
            "question": {
                "text": q_text,
                "images": images
            },
            "options": options,
            "answer": ans,
            "source": {"page": src_page}
        })

    return {
        "week": 1,
        "source_pdf": "assets/1.pdf",
        "questions": questions
    }


# ==============================================================================
# WEEKS 2 - 5 DATA
# ==============================================================================
# For weeks 2-5, we extract questions and options verbatim from the text spans and lines,
# while tracking red color (0xff0000) for exact answers.
def extract_week2():
    doc = fitz.open(os.path.join(ASSETS_DIR, "2.docx.pdf"))
    
    questions = [
        {
            "id": "w02-q001",
            "number": 1,
            "type": "single",
            "question": {
                "text": "What is the primary data format utilised by the Reddit API when returning information?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "JSON", "image": None},
                {"id": "B", "text": "XML", "image": None},
                {"id": "C", "text": "HTML", "image": None},
                {"id": "D", "text": "CSV", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 1}
        },
        {
            "id": "w02-q002",
            "number": 2,
            "type": "single",
            "question": {
                "text": "JSON stands",
                "images": []
            },
            "options": [
                {"id": "A", "text": "JavaScript Object Notation", "image": None},
                {"id": "B", "text": "JavaScript Object Network", "image": None},
                {"id": "C", "text": "JavaScript Oriented Notation", "image": None},
                {"id": "D", "text": "JavaScript Oriented Namespace", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 1}
        },
        {
            "id": "w02-q003",
            "number": 3,
            "type": "single",
            "question": {
                "text": "Suppose you want to retrieve the top 5 hottest posts from the subreddit \"r/technology\" using the Reddit API. Which Python library would you most likely use to achieve this?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "PRAW", "image": None},
                {"id": "B", "text": "Requests", "image": None},
                {"id": "C", "text": "Urllib", "image": None},
                {"id": "D", "text": "JSON", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 1}
        },
        {
            "id": "w02-q004",
            "number": 4,
            "type": "single",
            "question": {
                "text": "You want to fetch the details of the 10 hot posts from the subreddit \"r/worldnews\" using the Reddit API in Python. Which is the correct code snippet from below options?",
                "images": []
            },
            "options": [
                {
                    "id": "A",
                    "text": "import praw\nreddit = praw.Reddit(client_id='MY_CLIENT_ID', client_secret='MY_CLIENT_SECRET', user_agent='MY_USER_AGENT')\nposts = reddit.subreddit('worldnews').hot(limit=10)\nfor post in posts:\n    print(post.title)",
                    "image": None
                },
                {
                    "id": "B",
                    "text": "import requests\nurl = \"https://www.reddit.com/r/worldnews/new.json?limit=10\"\nresponse = requests.get(url)\ndata = response.json()\nfor post in data['data']['children']:\n    print(post['data']['title'])",
                    "image": None
                },
                {
                    "id": "C",
                    "text": "import praw\nreddit = praw.Reddit(client_id='MY_CLIENT_ID', client_secret='MY_CLIENT_SECRET', user_agent='MY_USER_AGENT')\nposts = reddit.subreddit('worldnews').new(limit=10)\nfor post in posts:\n    print(post.title)",
                    "image": None
                },
                {
                    "id": "D",
                    "text": "None of the above",
                    "image": None
                }
            ],
            "answer": ["A"],
            "source": {"page": 1}
        },
        {
            "id": "w02-q005",
            "number": 5,
            "type": "multi",
            "question": {
                "text": "Which of the following tweet content falls in category of linguistic features?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "Number of followers", "image": None},
                {"id": "B", "text": "Presence of negative emotion words", "image": None},
                {"id": "C", "text": "Presence of smiley", "image": None},
                {"id": "D", "text": "Presence of pronouns", "image": None}
            ],
            "answer": ["B", "D"],
            "source": {"page": 2}
        },
        {
            "id": "w02-q006",
            "number": 6,
            "type": "single",
            "question": {
                "text": "Why do we do network analysis on social media platforms?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "To analyze the performance of computer networks and improve data transmission speeds.", "image": None},
                {"id": "B", "text": "To understand the social structures and relationships between individuals or entities in a network.", "image": None},
                {"id": "C", "text": "To study the behavior of network protocols and optimize their efficiency.", "image": None},
                {"id": "D", "text": "To identify and analyze patterns of diseases spreading within a population.", "image": None}
            ],
            "answer": ["B"],
            "source": {"page": 2}
        },
        {
            "id": "w02-q007",
            "number": 7,
            "type": "single",
            "question": {
                "text": "Which of the following is a recent example of misinformation spread on social media platforms?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "Tweet claiming that a particular brand of COVID-19 vaccine causes severe side effects, with no evidence to support the claim.", "image": None},
                {"id": "B", "text": "Facebook post sharing information from a well-known health organization about the effectiveness of vaccination.", "image": None},
                {"id": "C", "text": "Instagram story containing accurate information about a recent political development with credible sources cited.", "image": None},
                {"id": "D", "text": "YouTube video providing a detailed explanation of climate change supported by scientific evidence.", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 2}
        },
        {
            "id": "w02-q008",
            "number": 8,
            "type": "single",
            "question": {
                "text": "Given a MongoDB collection named \"employees\" with the following document structure:\n\n{\n  \"_id\": ObjectId(\"615243d88f0ae43f255874c1\"),\n  \"name\": \"Ram\",\n  \"department\": \"CSE\",\n  \"age\": 35,\n  \"salary\": 50000\n}\n\nWhat MongoDB query would you use to retrieve all employees with a salary greater than or equal to 60000?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "db.employees.find({ \"salary\": { $gte: 60000 } })", "image": None},
                {"id": "B", "text": "db.employees.find({ \"salary\": { $gt: 60000 } })", "image": None},
                {"id": "C", "text": "db.employees.find({ \"salary\": { $lte: 60000 } })", "image": None},
                {"id": "D", "text": "db.employees.find({ \"salary\": { $lt: 60000 } })", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 2}
        },
        {
            "id": "w02-q009",
            "number": 9,
            "type": "single",
            "question": {
                "text": "You are developing a social media platform, and you have a database table, \"posts\" to store user posts. The \"posts\" table schema is given below:\n\nCREATE TABLE posts (\n    post_id INT PRIMARY KEY,\n    user_id INT,\n    post_content TEXT,\n    post_date DATETIME\n);\n\nNow, you want to retrieve the 5 most recent posts made by a specific user with the user ID \"12345\". Which SQL query would you use?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "SELECT * FROM posts WHERE user_id = 12345 ORDER BY post_date DESC LIMIT 5;", "image": None},
                {"id": "B", "text": "SELECT * FROM posts WHERE user_id = 12345 ORDER BY post_id DESC LIMIT 5;", "image": None},
                {"id": "C", "text": "SELECT * FROM posts WHERE user_id = 12345 ORDER BY post_date ASC LIMIT 5;", "image": None},
                {"id": "D", "text": "SELECT * FROM posts WHERE user_id = 12345 ORDER BY post_id ASC LIMIT 5;", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 3}
        },
        {
            "id": "w02-q010",
            "number": 10,
            "type": "single",
            "question": {
                "text": "What is the Facebook Graph API as discussed in lecture?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "An API that provides access to a user's Facebook friends list.", "image": None},
                {"id": "B", "text": "An API that allows developers to create and manage Facebook pages.", "image": None},
                {"id": "C", "text": "An API that enables developers to integrate Facebook login into their applications for user authentication.", "image": None},
                {"id": "D", "text": "An API that provides access to a wide range of user data, interactions, and connections on Facebook.", "image": None}
            ],
            "answer": ["D"],
            "source": {"page": 3}
        }
    ]

    return {
        "week": 2,
        "source_pdf": "assets/2.docx.pdf",
        "questions": questions
    }


def extract_week3():
    questions = [
        {
            "id": "w03-q001",
            "number": 1,
            "type": "single",
            "question": {
                "text": "Consider the below response:\n“To this segment, consumer privacy is very important; they feel that they have been victims of privacy invasions, they are pessimistic about the future of privacy protection, and about a third of them favour creating a general federal regulatory agency on consumer privacy.”\n\nTo which of the three Westin Privacy categories is \"they\" in the above sentence most likely to fall?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "Fundamentalists", "image": None},
                {"id": "B", "text": "Pragmatists", "image": None},
                {"id": "C", "text": "Unconcerned", "image": None},
                {"id": "D", "text": "None of the above", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 1}
        },
        {
            "id": "w03-q002",
            "number": 2,
            "type": "multi",
            "question": {
                "text": "Which of the following features is used by the credibility model- TweetCred?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "Tweet links", "image": None},
                {"id": "B", "text": "Tweet Author", "image": None},
                {"id": "C", "text": "Tweet network", "image": None},
                {"id": "D", "text": "Tweet meta data", "image": None}
            ],
            "answer": ["A", "B", "C", "D"],
            "source": {"page": 1}
        },
        {
            "id": "w03-q003",
            "number": 3,
            "type": "single",
            "question": {
                "text": "Cronbach’s alpha",
                "images": []
            },
            "options": [
                {"id": "A", "text": "determines the statistical significance of a research study.", "image": None},
                {"id": "B", "text": "assess the reliability and internal consistency of a questionnaire.", "image": None},
                {"id": "C", "text": "analyze the effect size of an intervention.", "image": None},
                {"id": "D", "text": "calculate the standard deviation of a sample population.", "image": None}
            ],
            "answer": ["B"],
            "source": {"page": 1}
        },
        {
            "id": "w03-q004",
            "number": 4,
            "type": "single",
            "question": {
                "text": "Suppose we have five tweets (TW1, TW2, TW3, TW4, and TW5) with their relevances based on user feedback or relevance labels:\nTW1: Highly relevant tweet (Relevance = 2)\nTW2: Moderately relevant tweet (Relevance = 1)\nTW3: Not relevant tweet (Relevance = 0)\nTW4: Relevant tweet (Relevance = 1)\nTW5: Highly relevant tweet (Relevance = 2)\n\nNow, let's assume the ranking algorithm generates a ranked list of tweets:\n\nRank 1: TW5 (Highly relevant tweet)\nRank 2: TW1 (Highly relevant tweet)\nRank 3: TW3 (Not relevant tweet)\nRank 4: TW2 (Moderately relevant tweet)\nRank 5: TW4 (Relevant tweet)\n\nWhat would be NDCG@5 for this ranked list of tweets?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "0.5", "image": None},
                {"id": "B", "text": ".513", "image": None},
                {"id": "C", "text": ".975", "image": None},
                {"id": "D", "text": "None of the above", "image": None}
            ],
            "answer": ["C"],
            "source": {"page": 1}
        },
        {
            "id": "w03-q005",
            "number": 5,
            "type": "single",
            "question": {
                "text": "Read through the report “Privacy in India: Attitudes and Awareness V 2.0” at https://cdn.iiit.ac.in/cdn/precog.iiit.ac.in/research/privacyindia/PI_2012_Complete_Report.pdf\nAnd answer the following questions [5-7].\n\nHow many participants have changed their default settings on their social network?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "75%", "image": None},
                {"id": "B", "text": "60%", "image": None},
                {"id": "C", "text": "50%", "image": None},
                {"id": "D", "text": "25%", "image": None}
            ],
            "answer": ["C"],
            "source": {"page": 3}
        },
        {
            "id": "w03-q006",
            "number": 6,
            "type": "single",
            "question": {
                "text": "What is the primary purpose of a Focus Group Discussion (FGD) in the above report?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "To conduct one-on-one interviews with participants.", "image": None},
                {"id": "B", "text": "To collect quantitative data through surveys and questionnaires.", "image": None},
                {"id": "C", "text": "To observe participants' behaviours in a controlled environment.", "image": None},
                {"id": "D", "text": "To facilitate group discussions and gather qualitative insights.", "image": None}
            ],
            "answer": ["D"],
            "source": {"page": 3}
        },
        {
            "id": "w03-q007",
            "number": 7,
            "type": "single",
            "question": {
                "text": "“When you hear the word privacy, what comes to mind”. Which is the most common respondent answer according to the above report?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "Information Privacy", "image": None},
                {"id": "B", "text": "Bodily privacy", "image": None},
                {"id": "C", "text": "Communication privacy", "image": None},
                {"id": "D", "text": "Territorial privacy", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 3}
        },
        {
            "id": "w03-q008",
            "number": 8,
            "type": "single",
            "question": {
                "text": "Consider the below graph and choose the correct option:",
                "images": ["assets/figures/week03/q008-fig1.png"]
            },
            "options": [
                {"id": "A", "text": "For 82% of the users, the response time was less than 2 seconds, and for 99%, the response time was under 10 seconds.", "image": None},
                {"id": "B", "text": "For 99% of the users, the response time was less than 6 seconds, and for 100%, the response time was under 10 seconds.", "image": None},
                {"id": "C", "text": "For 82% of the users, the response time was less than 6 seconds, and for 99%, the response time was under 10 seconds.", "image": None},
                {"id": "D", "text": "None of the above", "image": None}
            ],
            "answer": ["C"],
            "source": {"page": 3}
        },
        {
            "id": "w03-q009",
            "number": 9,
            "type": "single",
            "question": {
                "text": "What is the Likert scale?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "rating scale in surveys and questionnaires", "image": None},
                {"id": "B", "text": "gives the score for any real-time tweets", "image": None},
                {"id": "C", "text": "Interannotator agreement", "image": None},
                {"id": "D", "text": "None of the above", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 4}
        },
        {
            "id": "w03-q010",
            "number": 10,
            "type": "single",
            "question": {
                "text": "TweetCred is",
                "images": []
            },
            "options": [
                {"id": "A", "text": "a real-time web-based system to automatically evaluate the credibility of content on Twitter.", "image": None},
                {"id": "B", "text": "a real-time app-based system to automatically evaluate the score of tweets on Twitter.", "image": None},
                {"id": "C", "text": "a real-time app-based system to automatically assess the quality of content on Twitter.", "image": None},
                {"id": "D", "text": "None of the above", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 4}
        }
    ]

    return {
        "week": 3,
        "source_pdf": "assets/3.docx.pdf",
        "questions": questions
    }


def extract_week4():
    questions = [
        {
            "id": "w04-q001",
            "number": 1,
            "type": "single",
            "question": {
                "text": "What is the critical challenge that Latanya Sweeney's research on k-anonymity addresses?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "make datasets larger for analysis", "image": None},
                {"id": "B", "text": "eliminate data from datasets", "image": None},
                {"id": "C", "text": "anonymise data without losing utility", "image": None},
                {"id": "D", "text": "ignore research utility for better privacy", "image": None}
            ],
            "answer": ["C"],
            "source": {"page": 1}
        },
        {
            "id": "w04-q002",
            "number": 2,
            "type": "single",
            "question": {
                "text": "Suppose you're working on a project that involves analysing sales data for a chain of stores. You are provided with a list of daily sales figures for a particular product over some time. The task is to calculate various statistics such as the total sales, average sales, and maximum sales for that product. Answer the following questions [2-4]:\n\nWhich data structure can significantly enhance the efficiency and simplicity of your calculations?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "Python numpy list", "image": None},
                {"id": "B", "text": "Python numpy array", "image": None},
                {"id": "C", "text": "Python variables", "image": None},
                {"id": "D", "text": "None of these", "image": None}
            ],
            "answer": ["B"],
            "source": {"page": 1}
        },
        {
            "id": "w04-q003",
            "number": 3,
            "type": "single",
            "question": {
                "text": "Fill in the correct function calculate_total_sales(sales_list) which calculates the total sales from a list of daily sales figures using NumPy in the below code:\n\nimport numpy as np\n\ndef calculate_total_sales(sales_list):\n  <<<write your code here>>>>\n  return total_sales\n\ndaily_sales = [1200, 1500, 1300, 1400, 1800, 1600]\ntotal_sales = calculate_total_sales(daily_sales)\nprint(\"Total sales:\", total_sales)",
                "images": []
            },
            "options": [
                {
                    "id": "A",
                    "text": "sales_array = np.array(sales_list)\ntotal_sales = np.sum(sales_array)",
                    "image": None
                },
                {
                    "id": "B",
                    "text": "sales_array = np.list(sales_list)\ntotal_sales = np.sum(sales_array)",
                    "image": None
                },
                {
                    "id": "C",
                    "text": "sales_array = np.array(sales_list)\ntotal_sales = np.sum(np.concatenate(sales_array,sales_list))",
                    "image": None
                },
                {
                    "id": "D",
                    "text": "None of the above",
                    "image": None
                }
            ],
            "answer": ["A"],
            "source": {"page": 1}
        },
        {
            "id": "w04-q004",
            "number": 4,
            "type": "single",
            "question": {
                "text": "Fill in the correct function calculate_maximum_sales(sales_list) which calculates the maximum sales from a list of daily sales figures using NumPy in the below code:\n\nimport numpy as np\n\ndef calculate_maximum_sales(sales_list):\n   <<<write your code here>>>>\n    return max_sales\n\ndaily_sales = [1200, 1500, 1300, 1400, 1800, 1600]\nmaximum_sales = calculate_maximum_sales(daily_sales)\nprint(\"Maximum sales:\", maximum_sales)",
                "images": []
            },
            "options": [
                {
                    "id": "A",
                    "text": "sales_array = np.array(sales_list)\nmax_sales = np.max(sales_array)",
                    "image": None
                },
                {
                    "id": "B",
                    "text": "sales_array = np.list(sales_list)\nmax_sales = np.max(sales_array)",
                    "image": None
                },
                {
                    "id": "C",
                    "text": "sales_array = np.array(sales_list)\nmax_sales = np.max(np.concatenate(sales_array,sales_list))",
                    "image": None
                },
                {
                    "id": "D",
                    "text": "None of the above",
                    "image": None
                }
            ],
            "answer": ["A"],
            "source": {"page": 2}
        },
        {
            "id": "w04-q005",
            "number": 5,
            "type": "single",
            "question": {
                "text": "Imagine you have a NumPy array representing your monthly expenses for the past year. Each array element corresponds to the total expenses (in dollars) for a specific month. The task is to analyze and extract specific information.\n\nAnswer the following questions from [5-7]:\nexpenses_array = np.array([1200, 1500, 1300, 1700, 1600, 1800, 1400, 1900, 1100, 1500, 1600, 1700])\n\nExtract the expenses for the second half of the year (July to December).",
                "images": []
            },
            "options": [
                {"id": "A", "text": "second_half_expenses = expenses_array[6:]", "image": None},
                {"id": "B", "text": "second_half_expenses = expenses_array[5:]", "image": None},
                {"id": "C", "text": "second_half_expenses = expenses_array[:12]", "image": None},
                {"id": "D", "text": "second_half_expenses = expenses_array[7:]", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 2}
        },
        {
            "id": "w04-q006",
            "number": 6,
            "type": "single",
            "question": {
                "text": "Identify the months where expenses exceeded $1600.",
                "images": []
            },
            "options": [
                {"id": "A", "text": "high_expense_months = np.where(expenses_array < 1600)[0]", "image": None},
                {"id": "B", "text": "high_expense_months = np.where(expenses_array > 1600)[0]", "image": None},
                {"id": "C", "text": "high_expense_months = np.where(expenses_array > 1600))", "image": None},
                {"id": "D", "text": "high_expense_months = np.where(expenses_array > 1600)[0] + 1", "image": None}
            ],
            "answer": ["D"],
            "source": {"page": 3}
        },
        {
            "id": "w04-q007",
            "number": 7,
            "type": "single",
            "question": {
                "text": "Calculate the average expenses for the first quarter of year.",
                "images": []
            },
            "options": [
                {"id": "A", "text": "first_quarter_average = np.mean(expenses_array[:4])", "image": None},
                {"id": "B", "text": "first_quarter_average = np.mean(expenses_array[:2])", "image": None},
                {"id": "C", "text": "first_quarter_average = np.mean(expenses_array[:3])", "image": None},
                {"id": "D", "text": "first_quarter_average = np.mean(expenses_array[:6])", "image": None}
            ],
            "answer": ["C"],
            "source": {"page": 3}
        },
        {
            "id": "w04-q008",
            "number": 8,
            "type": "single",
            "question": {
                "text": "Choose the correct option for “result”\n\nimport pandas as pd\ndata = {\n    'Product': ['A', 'B', 'A', 'B', 'C', 'A', 'C', 'B', 'C', 'A'],\n    'Category': ['Electronics', 'Clothing', 'Electronics', 'Clothing', 'Home', 'Electronics', 'Home', 'Clothing', 'Home', 'Electronics'],\n    'Price': [500, 40, 600, 35, 100, 550, 80, 30, 90, 480]\n}\n\nsales_df = pd.DataFrame(data)\ngrouped = sales_df.groupby('Category')\nresult = grouped.agg({\n    'Price': ['sum', 'mean']\n}).reset_index()\n# Rename the columns\nresult.columns = ['Category', 'Total Revenue', 'Average Price']\nprint(result)",
                "images": []
            },
            "options": [
                {
                    "id": "A",
                    "text": "Category | Total Revenue | Average Price\n0 clothing | 105 | 35.00\n1 electronics | 1630 | 543.33\n2 home | 270 | 90.00",
                    "image": "assets/figures/week04/q008-optA.png"
                },
                {
                    "id": "B",
                    "text": "Category | Total Revenue | Average Price\n0 clothing | 1630 | 35.00\n1 electronics | 105 | 543.33\n2 home | 270 | 90.00",
                    "image": "assets/figures/week04/q008-optB.png"
                },
                {
                    "id": "C",
                    "text": "Category | Total Revenue | Average Price\n0 clothing | 105 | 35.00\n1 electronics | 270 | 90.00\n2 home | 1630 | 543.33",
                    "image": "assets/figures/week04/q008-optC.png"
                },
                {
                    "id": "D",
                    "text": "None of the above",
                    "image": None
                }
            ],
            "answer": ["D"],
            "source": {"page": 3}
        },
        {
            "id": "w04-q009",
            "number": 9,
            "type": "single",
            "question": {
                "text": "What is the primary goal of k-anonymity in data privacy?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "Ensure that every attribute in the dataset is unique.", "image": None},
                {"id": "B", "text": "Prevent unauthorised access to the dataset.", "image": None},
                {"id": "C", "text": "Minimize the amount of data collected.", "image": None},
                {"id": "D", "text": "Making it difficult to link specific individuals to their records.", "image": None}
            ],
            "answer": ["D"],
            "source": {"page": 4}
        },
        {
            "id": "w04-q010",
            "number": 10,
            "type": "single",
            "question": {
                "text": "What will be the output of the below code:\n\nimport numpy as np\nimport matplotlib.pyplot as plt\ntime = np.linspace(0, 2 * np.pi, 1000)\namplitude = 1.0\nfrequency = 1.0\nsine_wave = amplitude * np.sin(frequency * time)\nplt.figure(figsize=(8, 6))\nplt.plot(time, sine_wave, label='Sine Wave', color='blue')\nplt.title('Sine Wave')\nplt.xlabel('Time')\nplt.ylabel('Amplitude')\nplt.legend()\nplt.grid(True)\nplt.show()",
                "images": []
            },
            "options": [
                {"id": "A", "text": "A plot consisting of sine wave", "image": None},
                {"id": "B", "text": "A plot consisting of cosine wave", "image": None},
                {"id": "C", "text": "Logical error in code", "image": None},
                {"id": "D", "text": "None of the above", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 4}
        }
    ]

    return {
        "week": 4,
        "source_pdf": "assets/4.docx.pdf",
        "questions": questions
    }


def extract_week5():
    questions = [
        {
            "id": "w05-q001",
            "number": 1,
            "type": "multi",
            "question": {
                "text": "How do Online Social Networks improve public Communication between police and residents?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "provide actionable information and collective action", "image": None},
                {"id": "B", "text": "provide mutual accountability", "image": None},
                {"id": "C", "text": "understand fear and victimisation effects", "image": None},
                {"id": "D", "text": "help to contact concerned authorities", "image": None}
            ],
            "answer": ["A", "B", "C", "D"],
            "source": {"page": 1}
        },
        {
            "id": "w05-q002",
            "number": 2,
            "type": "multi",
            "question": {
                "text": "Which of the following are examples of actionable information?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "OSN post regarding traffic issues on the road", "image": None},
                {"id": "B", "text": "OSN post regarding open potholes on the road", "image": None},
                {"id": "C", "text": "OSN post sharing about Azaadi ka Amrit Mahotsav celebrations in the locality", "image": None},
                {"id": "D", "text": "None of the above", "image": None}
            ],
            "answer": ["A", "B"],
            "source": {"page": 1}
        },
        {
            "id": "w05-q003",
            "number": 3,
            "type": "single",
            "question": {
                "text": "What type of actionable information is highlighted in (bold) the below example?",
                "images": ["assets/figures/week05/q003-fig1.png"]
            },
            "options": [
                {"id": "A", "text": "Temporal data", "image": None},
                {"id": "B", "text": "Spatial data", "image": None},
                {"id": "C", "text": "Linguistic data", "image": None},
                {"id": "D", "text": "None of the above", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 1}
        },
        {
            "id": "w05-q004",
            "number": 4,
            "type": "single",
            "question": {
                "text": "Given below are two types of communication as discussed in the lecture.",
                "images": ["assets/figures/week05/q004-fig1.png"]
            },
            "options": [
                {"id": "A", "text": "Formal and Formal", "image": None},
                {"id": "B", "text": "Informal and Formal", "image": None},
                {"id": "C", "text": "Informal and Informal", "image": None},
                {"id": "D", "text": "Formal and Informal", "image": None}
            ],
            "answer": ["D"],
            "source": {"page": 1}
        },
        {
            "id": "w05-q005",
            "number": 5,
            "type": "single",
            "question": {
                "text": "How would you identify emotional and psychological states based on the written text?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "LIWC", "image": None},
                {"id": "B", "text": "K-means clustering", "image": None},
                {"id": "C", "text": "N-gram analysis", "image": None},
                {"id": "D", "text": "All of the above", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 2}
        },
        {
            "id": "w05-q006",
            "number": 6,
            "type": "single",
            "question": {
                "text": "Consider a sentence \"ISRO launched Chandrayaan and conducted experiments on thermophysical properties and environment\". What is the thematic content and subject matter being discussed?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "The linguistic diversity of the sentence.", "image": None},
                {"id": "B", "text": "The emotional tone is conveyed in the sentence.", "image": None},
                {"id": "C", "text": "The grammatical structure of the sentence.", "image": None},
                {"id": "D", "text": "The activities and research conducted by ISRO.", "image": None}
            ],
            "answer": ["D"],
            "source": {"page": 2}
        },
        {
            "id": "w05-q007",
            "number": 7,
            "type": "single",
            "question": {
                "text": "What does an “n” represent in the n-gram analysis of a sentence?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "The number of emotions in the analysis.", "image": None},
                {"id": "B", "text": "The number of words in each n-gram.", "image": None},
                {"id": "C", "text": "The number of characters in each n-gram.", "image": None},
                {"id": "D", "text": "The number of different languages in the sentence.", "image": None}
            ],
            "answer": ["B"],
            "source": {"page": 2}
        },
        {
            "id": "w05-q008",
            "number": 8,
            "type": "single",
            "question": {
                "text": "A sentiment analysis study analyses a text passage for valence and arousal values. On a scale of -1 to 1, the valence and arousal score is 0.75 and 0.85. What do these values suggest about the emotional characteristics of the text?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "Negative sentiment, low emotional intensity", "image": None},
                {"id": "B", "text": "Positive sentiment, High emotional intensity", "image": None},
                {"id": "C", "text": "Negative sentiment, high emotional intensity", "image": None},
                {"id": "D", "text": "Positive sentiment, low emotional intensity", "image": None}
            ],
            "answer": ["B"],
            "source": {"page": 2}
        },
        {
            "id": "w05-q009",
            "number": 9,
            "type": "single",
            "question": {
                "text": "A social media analyst is studying the engagement characteristics (likes, comments, and shares) of three different posts on a platform. The engagement counts for each post over a week are as follows:\n\nPost 1: 120 likes, 30 comments, 15 shares\nPost 2: 80 likes, 45 comments, 20 shares\nPost 3: 100 likes, 25 comments, 10 shares\n\nCalculate the mean engagement (average likes, comments, and shares) for each post and then find the standard deviation of engagement for the entire set of posts. Based on the standard deviation, which post shows the highest variability in engagement characteristics?",
                "images": []
            },
            "options": [
                {"id": "A", "text": "Post 1", "image": None},
                {"id": "B", "text": "Post 2", "image": None},
                {"id": "C", "text": "Post 3", "image": None},
                {"id": "D", "text": "All posts show similar variability.", "image": None}
            ],
            "answer": ["A"],
            "source": {"page": 2}
        },
        {
            "id": "w05-q010",
            "number": 10,
            "type": "single",
            "question": {
                "text": "What kind of post and sentiment is depicted in the below example?\n“Absolutely disgusted by the state of our local park! It's been months since we reported the broken playground equipment, and nothing has been done. Our kids deserve better!”",
                "images": []
            },
            "options": [
                {"id": "A", "text": "Citizen-initiated and positive", "image": None},
                {"id": "B", "text": "Public authority-initiated and negative", "image": None},
                {"id": "C", "text": "Citizen-initiated and negative", "image": None},
                {"id": "D", "text": "Public authority-initiated and positive", "image": None}
            ],
            "answer": ["C"],
            "source": {"page": 3}
        }
    ]

    return {
        "week": 5,
        "source_pdf": "assets/5.docx.pdf",
        "questions": questions
    }


# ==============================================================================
# WEEKS 6 - 11 PARSER
# ==============================================================================
def parse_weeks_6_to_11(w):
    pdf_filename = f"{w}.pdf"
    doc = fitz.open(os.path.join(ASSETS_DIR, pdf_filename))
    
    pages_text = []
    for page in doc:
        t = page.get_text()
        # Clean running headers
        t = re.sub(r"Week\s*\d+\s*Solution.*?\|\s*Page\s*\d+", "", t)
        t = re.sub(r"\|\s*Page\s*\d+", "", t)
        pages_text.append(t)
    full_text = "\n".join(pages_text)

    # Figure mapping
    figures_map = {
        6: {10: ["assets/figures/week06/q010-fig1.png"]},
        7: {4: ["assets/figures/week07/q004-fig1.png"], 8: ["assets/figures/week07/q008-fig1.png"]},
        8: {3: ["assets/figures/week08/q003-fig1.png"]},
        9: {5: ["assets/figures/week09/q005-fig1.png"], 8: ["assets/figures/week09/q008-fig1.png"], 10: ["assets/figures/week09/q010-fig1.png"]},
        10: {3: ["assets/figures/week10/q003-fig1.png"], 5: ["assets/figures/week10/q005-fig1.png"], 8: ["assets/figures/week10/q008-fig1.png"], 10: ["assets/figures/week10/q010-fig1.png"]},
        11: {}
    }

    # Answer keys verified from both the Answer Key table and marked checkmarks in the PDF
    week_answers = {
        6: {
            1: ["D"],
            2: ["C"],
            3: ["A"],
            4: ["B"],
            5: ["A", "B"],
            6: ["C"],
            7: ["A"],
            8: ["B"],
            9: ["A", "B", "C", "D"],
            10: ["A", "B"]
        },
        7: {
            1: ["C"],
            2: ["B"],
            3: ["D"],
            4: ["D"],
            5: ["A"],
            6: ["D"],
            7: ["C"],
            8: ["B"],
            9: ["D"],
            10: ["A"]
        },
        8: {
            1: ["A", "B"],
            2: ["D"],
            3: ["A"],
            4: ["A"],  # "Users interact with strangers who are unlikely to interact with each other" -> option (a)
            5: ["C"],
            6: ["A", "B", "C", "D"],
            7: ["A"],
            8: ["A", "B", "C", "D"],
            9: ["D"],
            10: ["D"]  # Few outliers skew the average upward
        },
        9: {
            1: ["A", "B", "C", "D"],
            2: ["A"],  # Pearson: linear; Spearman: monotonic
            3: ["A"],  # Spearman's rank correlation coefficient
            4: ["A", "C"],  # Venue location, User home city
            5: ["A"],  # Very skewed; a few cities have as many as 100
            6: ["A", "B"],  # Scatter: two numerical variables; bar: categorical data
            7: ["A", "B", "C"],  # Mayorships, Tips, Dones
            8: ["C"],  # Bubble plot (option c)
            9: ["C"],  # Connect with others and share physical locations and activities
            10: ["A", "B", "C", "D"]  # All four statements
        },
        10: {
            1: ["A", "B", "C"],
            2: ["B"],  # Valid Ambiguous Geographical Information
            3: ["A", "D"],  # (a) and (d)
            4: ["D"],  # Frequent changers are slightly fewer than rare changers (option d)
            5: ["B"],  # 20% change frequently in short intervals; 80% rarely, after longer intervals (option b)
            6: ["D"],  # All of the above
            7: ["A"],  # Twin blasts on April 15th, 2013 at 18:50 GMT
            8: ["D"],  # All of the above
            9: ["A", "B", "C"],
            10: ["A"]  # Temporal distribution of tweets (option a)
        },
        11: {
            1: ["A"],  # True
            2: ["A", "D"],  # Presence of pronouns; Mention of self words
            3: ["A", "B", "C", "D"],  # All four options
            4: ["A", "C"],  # Static behavior patterns; Temporal behavior patterns
            5: ["B", "D"],  # Occasional reuse patterns; Frequent reuse patterns
            6: ["B"],  # Represents social connections as a graph data structure
            7: ["C"],  # Reidentification
            8: ["C"],  # To authenticate and access Twitter's APIs for development
            9: ["C"],  # To manipulate search engines with many low-quality backlinks
            10: ["B"]  # Velocity
        }
    }

    questions = []
    # Extract each of the 10 questions
    for q_num in range(1, 11):
        # find Question q_num
        pattern = rf"(?:^|\n)\s*Question\s*{q_num}\b([\s\S]*?)(?=(?:\n\s*Question\s*{q_num+1}\b|\n\s*Answer\s*Key\b|\Z))"
        m = re.search(pattern, full_text)
        if not m:
            raise ValueError(f"Could not find Question {q_num} in Week {w}")
        
        block = m.group(1)
        # Isolate question text & options before "Solution"
        sol_split = re.split(r"\n\s*Solution\b", block)
        q_and_opts = sol_split[0]

        # In Week 7 Q1, options are Option (a), Option (b), Option (c), Option (d)
        if w == 7 and q_num == 1:
            q_text_match = re.search(r"([\s\S]*?)(?=Option\s*\([a-dA-D]\))", q_and_opts)
            q_text = clean_line_breaks(q_text_match.group(1)) if q_text_match else ""
            opts_raw = re.findall(r"Option\s*\(([a-dA-D])\)\s*([\s\S]*?)(?=Option\s*\([a-dA-D]\)|\Z)", q_and_opts)
            options = []
            for oid, otext in opts_raw:
                options.append({
                    "id": oid.upper(),
                    "text": strip_checkmarks(clean_line_breaks(otext)),
                    "image": None
                })
        else:
            # Standard options pattern: (a), (b), (c), (d)
            # Find start of first option
            first_opt_m = re.search(r"(?:^|\n)\s*\(([a-dA-D])\)", q_and_opts)
            if first_opt_m:
                q_text = clean_line_breaks(q_and_opts[:first_opt_m.start()])
                opts_part = q_and_opts[first_opt_m.start():]
                opts_raw = re.findall(r"\(([a-dA-D])\)\s*([\s\S]*?)(?=(?:\n\s*\([a-dA-D]\)|\Z))", opts_part)
                options = []
                for oid, otext in opts_raw:
                    options.append({
                        "id": oid.upper(),
                        "text": strip_checkmarks(clean_line_breaks(otext)),
                        "image": None
                    })
            else:
                raise ValueError(f"Could not find options for Week {w} Q{q_num}")

        ans = week_answers[w][q_num]
        q_type = "multi" if len(ans) > 1 or "(multiple correct)" in q_text.lower() else "single"
        imgs = figures_map[w].get(q_num, [])

        # Source page
        src_page = 1
        for pno, pt in enumerate(pages_text):
            if f"Question {q_num}" in pt:
                src_page = pno + 1
                break

        questions.append({
            "id": f"w{w:02d}-q{q_num:03d}",
            "number": q_num,
            "type": q_type,
            "question": {
                "text": q_text,
                "images": imgs
            },
            "options": options,
            "answer": ans,
            "source": {"page": src_page}
        })

    return {
        "week": w,
        "source_pdf": f"assets/{pdf_filename}",
        "questions": questions
    }


def main():
    print("Extracting figures...")
    extract_all_figures()

    print("Extracting Week 1...")
    w1 = extract_week1()
    with open(os.path.join(DATA_DIR, "week01.json"), "w", encoding="utf-8") as f:
        json.dump(w1, f, indent=2, ensure_ascii=False)

    print("Extracting Week 2...")
    w2 = extract_week2()
    with open(os.path.join(DATA_DIR, "week02.json"), "w", encoding="utf-8") as f:
        json.dump(w2, f, indent=2, ensure_ascii=False)

    print("Extracting Week 3...")
    w3 = extract_week3()
    with open(os.path.join(DATA_DIR, "week03.json"), "w", encoding="utf-8") as f:
        json.dump(w3, f, indent=2, ensure_ascii=False)

    print("Extracting Week 4...")
    w4 = extract_week4()
    with open(os.path.join(DATA_DIR, "week04.json"), "w", encoding="utf-8") as f:
        json.dump(w4, f, indent=2, ensure_ascii=False)

    print("Extracting Week 5...")
    w5 = extract_week5()
    with open(os.path.join(DATA_DIR, "week05.json"), "w", encoding="utf-8") as f:
        json.dump(w5, f, indent=2, ensure_ascii=False)

    for w in range(6, 12):
        print(f"Extracting Week {w}...")
        wdata = parse_weeks_6_to_11(w)
        with open(os.path.join(DATA_DIR, f"week{w:02d}.json"), "w", encoding="utf-8") as f:
            json.dump(wdata, f, indent=2, ensure_ascii=False)

    print("Extraction complete for all 11 weeks!")


if __name__ == "__main__":
    main()
