# app/model.py

from transformers import BartTokenizer, BartForConditionalGeneration
import torch

# Load model and tokenizer at module level (only once)
MODEL_NAME = "memray/bart_wikikp"
tokenizer = BartTokenizer.from_pretrained(MODEL_NAME)
model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

def generate_keywords(text: str, num_beams: int = 5, max_length: int = 60) -> list:
    """
    Generate keyphrases from input text using the BART model.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            num_beams=num_beams,
            max_length=max_length,
            early_stopping=True
        )
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return [kp.strip() for kp in decoded.split(";")]
