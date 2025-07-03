from transformers import T5ForConditionalGeneration, T5Tokenizer
import os
import torch

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model_t5")

tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)
model.eval()


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputText(BaseModel):
    text: str

@app.post("/convert/")
def convert_text(input_data: InputText):
    input_ids = tokenizer.encode("Formalize the text: " + input_data.text, return_tensors="pt")
    with torch.no_grad():
        output_ids = model.generate(input_ids, max_length=128, num_beams=4, early_stopping=True)
    output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return {"output": output}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your Django host
    allow_methods=["*"],
    allow_headers=["*"],
)