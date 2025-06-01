# app/utils.py

import pdfplumber
from fastapi import UploadFile
from typing import Optional, Tuple

def extract_title_and_abstract(file: UploadFile) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts the title and abstract from the first page of a scientific paper PDF.
    Returns (title, abstract) as a tuple of strings.
    """
    try:
        with pdfplumber.open(file.file) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()

        if not text:
            return None, None

        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Assume title is first non-empty line
        title = lines[0]

        # Heuristic: abstract follows the line "Abstract" or is the second paragraph
        abstract = ""
        found_abstract_heading = False
        for line in lines[1:]:
            if line.lower() in ["abstract", "abstract:"]:
                found_abstract_heading = True
                continue
            if found_abstract_heading:
                if line.lower().startswith("keywords") or line.lower().startswith("introduction"):
                    break
                abstract += " " + line
            elif not abstract and len(line.split()) > 20:
                # If there's no "Abstract" keyword, fall back to finding the next long paragraph
                abstract = line

        return title.strip(), abstract.strip()

    except Exception as e:
        print(f"❌ Error extracting text from PDF: {e}")
        return None, None
