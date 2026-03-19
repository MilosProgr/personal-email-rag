from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from config import LLM_MODEL_PATH

tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_PATH)

llm_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0  # 0 = GPU, -1 = CPU
)

def generate(prompt, max_length=256):
    """
    Generate text from prompt using local LLM.
    """
    output = llm_pipeline(prompt, max_length=max_length, do_sample=True)
    return output[0]['generated_text']