# src/llm_wrapper.py
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from config import LLM_MODEL_PATH

# Load local LLM
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_PATH, device_map="auto")

llm_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
     
      # 0=GPU, -1=CPU only when device map is not put
)


def generate(prompt, max_length=256, temperature=0.7):
    output = llm_pipeline(
        prompt,
        max_length=max_length,
        do_sample=True,
        temperature=temperature
    )
    return output[0]["generated_text"]