# app/utils.py

import pdfplumber
from fastapi import UploadFile
from typing import Optional, Tuple
import re

def extract_title_and_abstract(file: UploadFile):
    with pdfplumber.open(file.file) as pdf:
        full_text = ""
        for page in pdf.pages[:3]:  # reading first 3 pages
            full_text += page.extract_text(x_tolerance=1.5) + "\n"

    lines = full_text.splitlines()
    title = lines[0].strip()

    abstract_started = False
    abstract_lines = []

    for line in lines:
        if not abstract_started:
            if line.strip().lower() == "abstract":
                abstract_started = True
            continue

        # stopping the collecting if a new section starts
        if re.match(r"^(1\s+)?(introduction|keywords)\b", line.strip().lower()):
            break
        abstract_lines.append(line.strip())

    abstract = " ".join(abstract_lines)

    return title, abstract

