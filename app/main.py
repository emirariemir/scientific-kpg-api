# app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils import extract_title_and_abstract
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

@app.post("/extract")
async def extract_keywords(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    title, abstract = extract_title_and_abstract(file)

    if not title or not abstract:
        raise HTTPException(status_code=422, detail="Failed to extract title or abstract.")

    model_input = f"Title: {title}\nAbstract: {abstract}"
    keywords = generate_keywords(model_input)

    return {
        "title": title,
        "abstract": abstract,
        "keywords": keywords
    }
