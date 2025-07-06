# app/utils.py

import pdfplumber
from fastapi import UploadFile
from typing import Optional, Tuple
import re

def extract_abstract_text(file: UploadFile, is_two_column: bool = False) -> str:
    with pdfplumber.open(file.file) as pdf:
        full_text = ""

        for page in pdf.pages:
            if is_two_column:
                left = page.crop((0, 0, 0.5 * page.width, 0.9 * page.height))
                right = page.crop((0.5 * page.width, 0, page.width, page.height))

                l_text = left.extract_text(x_tolerance=1.5) or ""
                r_text = right.extract_text(x_tolerance=1.5) or ""

                page_text = l_text + "\n" + r_text
            else:
                page_text = page.extract_text(x_tolerance=1.5) or ""

            full_text += page_text + "\n"

        # Clean hyphenated line breaks
        full_text = re.sub(r'-\s*\n\s*', '', full_text)


    lines = full_text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    abstract_started = False
    abstract_lines = []

    for line in lines:
        lower_line = line.lower()

        if not abstract_started:
            if "abstract" in lower_line:
                abstract_started = True
            continue

        # Stop if line starts with a number or matches 'introduction' or 'keywords'
        if re.match(r"^\d", line) or lower_line.startswith("introduction") or lower_line.startswith("keywords") or lower_line.startswith("key words"):
            break

        abstract_lines.append(line)

    abstract = " ".join(abstract_lines).strip()

    # Optional: clean up extra spaces and special characters if needed
    abstract = re.sub(r"\s+", " ", abstract)
    return abstract
