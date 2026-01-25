from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI()

# Load model ONCE at startup
llm = Llama(
    model_path="models/qwen2.5-0.5b-instruct.gguf",
    n_ctx=1024,
    n_threads=4,
    verbose=False
)

class GenerateRequest(BaseModel):
    name: str
    age: str
    adjective: str
    hobby: str
    lang: str

@app.post("/generate")
def generate(req: GenerateRequest):
    prompt = f"""
You are a funny birthday card generator.

Language: {req.lang}
Name: {req.name}
Age: {req.age}
Adjective: {req.adjective}
Hobby: {req.hobby}

Rules:
- Write ONE short funny birthday message
- 1–2 sentences
- Friendly and playful
- No explanations
- No hashtags
"""

    output = llm(
        prompt,
        max_tokens=80,
        temperature=0.9,
        top_p=0.95,
        stop=["\n\n"]
    )

    text = output["choices"][0]["text"].strip()
    return {"message": text}