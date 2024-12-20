from transformers import pipeline, set_seed, AutoModelForCausalLM, AutoTokenizer
from fastapi import FastAPI
from pydantic import BaseModel

# Téléchargez et chargez le modèle
model_ckpt = 'transformersbook/codeparrot-small'
model = AutoModelForCausalLM.from_pretrained(model_ckpt)
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
generation = pipeline('text-generation', model=model, tokenizer=tokenizer, device=-1)

import re

def first_block(string):
    return re.split('\nclass|\ndef|\n#|\n@|\nprint|\nif', string)[0].rstrip()

def complete_code(pipe, prompt, max_length=64, num_completions=4, seed=1):
    set_seed(seed)
    gen_kwargs = {"temperature": 0.4, "top_p": 0.95, "top_k": 0, "num_beams": 1, "do_sample": True}
    code_gens = pipe(prompt, num_return_sequences=num_completions, max_length=max_length, **gen_kwargs)
    code_strings = []
    for code_gen in code_gens:
        generated_code = first_block(code_gen['generated_text'][len(prompt):])
        code_strings.append(generated_code)
    return code_strings

class CodeRequest(BaseModel):
    prompt: str

class CodeResponse(BaseModel):
    generated_code: list

app = FastAPI()

@app.post("/generate-code", response_model=CodeResponse)
def generate_code(request: CodeRequest):
    generated_code = complete_code(generation, request.prompt)
    return CodeResponse(generated_code=generated_code)

@app.get("/test")
def generate_code():
    return "test api"


@app.get("/generate-code")
def generate_code():
    prompt = '''def addtonumbers(a: float, b: float):
    """Return the some of two numbers."""'''
    generated_code = complete_code(generation,prompt)
    return CodeResponse(generated_code=generated_code)