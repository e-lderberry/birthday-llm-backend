from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI()

# Load model ONCE at startup
llm = Llama(
    model_path="models/qwen2.5-0.5b-instruct.gguf",
    n_ctx=1024,
    n_threads=2,
    # verbose=False
)

# warm-up to avoid first-request timeout
llm("Hello", max_tokens=1)

class GenerateRequest(BaseModel):
    name: str
    age: str
    adjective: str
    hobby: str
    lang: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/generate")
def generate(req: GenerateRequest):
    prompt = f"""
Write a birthday card message.

Write the ACTUAL birthday message text.
Do NOT explain anything.
Do NOT write rules or lists.
Do NOT evaluate anything.

Language: {req.lang}

Details to include naturally:
- Name: {req.name}
- Age: {req.age}
- Adjective: {req.adjective}
- Hobby: {req.hobby}

Write ONE short funny birthday message (1–2 sentences).
Output ONLY the message text.
"""

    output = llm(
        prompt,
        max_tokens=80,
        temperature=0.9,
        top_p=0.95,
        stop=["<|im_end|>", "\n", "-"]
    )

    text = output["choices"][0]["text"].strip()
    return {"message": text}