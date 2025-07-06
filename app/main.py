# app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from app.utils import extract_abstract_text
from app.model import generate_keywords

app = FastAPI(
    title="KPG Keyword Extractor API",
    description="Extracts keyphrases from scientific white papers using a pretrained BART model.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-keywords/")
async def extract_keywords(file: UploadFile = File(...), is_two_column: bool = False):
    text = extract_abstract_text(file, is_two_column)
    keywords = generate_keywords(text)
    return {"keywords": keywords}
