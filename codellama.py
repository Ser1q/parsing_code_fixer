from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "codellama/CodeLlama-7b-Instruct-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map={"": "cpu"})
tokenizer.model_max_length = 16384 # Setting correct value for max tokens


def generate_prompt_for_html_diff(html_old: str, html_new: str) -> str:
    return f"""### Instruction:
You are an AI assistant that compares two HTML files and explains the structural and content differences between them.

### Old HTML:
{html_old}

### New HTML:
{html_new}

### Task:
List the structural changes step by step. Focus on:
- Tags that were added or removed
- Class or attribute changes
- Text changes
- Moved sections

### Differences:"""

def get_html_differences(html_old: str, html_new: str, max_tokens=1024):
    prompt = generate_prompt_for_html_diff(html_old, html_new)
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=inputs["input_ids"].shape[1] + max_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            eos_token_id=tokenizer.eos_token_id
        )
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result.split("### Differences:")[-1].strip()