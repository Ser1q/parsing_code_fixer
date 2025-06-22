import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
# from bs4 import BeautifulSoup, Comment

def generate_function_iteratively(prompt, max_new_tokens=1024, max_iters=1):
    model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map={"": "cpu"})

    tokenizer.model_max_length = 16384 # Setting correct value for max tokens

    device = model.device
    generated = prompt
    for i in range(max_iters):
        inputs = tokenizer(generated, return_tensors="pt", truncation=True).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.3,
                top_p=0.95,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        new_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Only get the new part (remove prompt overlap)
        new_part = new_text[len(generated):]
        generated += new_part

        print(f"[Chunk {i+1}]:\n{new_part}\n{'-'*40}")

        # Heuristic to stop if function likely finished (e.g., next def/class or end of indentation)
        if '\ndef ' in new_part or '\nclass ' in new_part or new_part.strip().endswith("return") or new_part.strip().endswith("]"):
            break

    return generated

def generate_prompt_for_deepseek(old_code: str, changed_html: str) -> str:
    prompt = f"""You are a Python expert working with BeautifulSoup.
The following Python code was originally written to parse a webpage. However, the structure of the HTML has changed.
Your task is to update the code to match the changes in HTML structure while keeping the same logic and variable names.
---
Changes in HTML structure:
{changed_html.strip()}
---
Original Python code:
{old_code.strip()}
Please provide the corrected version of the Python code that works with the updated HTML structure.
Only output the updated code, without explanations or extra text.
"""
    return prompt
    
