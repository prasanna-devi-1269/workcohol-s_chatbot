import os
import json
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import utils

load_dotenv()
app = FastAPI()

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load Gemini & Hugging Face
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_KEY"))
gemini_model = genai.GenerativeModel(model_name="gemini-pro")

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model_hf = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
hf_pipeline = pipeline("text2text-generation", model=model_hf, tokenizer=tokenizer)

# Load base data
with open("sample.json", "r", encoding="utf-8") as f:
    base_data = json.load(f)

# Request format
class ChatRequest(BaseModel):
    query: str
    user_file: str | None = None

@app.post("/chat/")
async def chat_endpoint(req: ChatRequest):
    context = utils.search_json_data(req.query, base_data)
    if req.user_file:
        context += "\n\n" + req.user_file

    prompt = f"Context:\n{context}\n\nQuestion:\n{req.query}\n\nAnswer:"
    try:
        gemini_response = gemini_model.generate_content(prompt)
        return {"response": gemini_response.text.strip()}
    except:
        fallback = hf_pipeline(prompt, max_length=200, do_sample=True)
        return {"response": fallback[0]["generated_text"].strip()}
