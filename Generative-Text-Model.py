# %%
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import logging as hf_logging
import warnings
import os
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
hf_logging.set_verbosity_error()

# %%
def load_model():
    print("Loading model... (this may take a moment on the first run)")
    model_id = 'Qwen/Qwen2.5-0.5B-Instruct'
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    return tokenizer, model

# %%
def generate_text(tokenizer, model, prompt):
    if not prompt.strip():
        return "Prompt cannot be empty."
        
    messages = [
        {"role": "system", "content": "You are an expert writer. Write a coherent, informative paragraph about the given topic."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt")
    
    outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.7, do_sample=True)
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, outputs)]
    answer = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return answer

# %%
if __name__ == "__main__":
    tokenizer, model = load_model()
    
    in_jupyter = 'ipykernel' in sys.modules
    
    prompt = ""
    if not in_jupyter and len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        try:
            prompt = input("\nEnter your topic or prompt: ")
        except EOFError:
            prompt = "The future of artificial intelligence in healthcare"
            print(f"\nUsing default prompt: {prompt}")
            
    print(f"\nPrompt: {prompt}")
    answer = generate_text(tokenizer, model, prompt)
    
    print("\n--- Generated Text ---")
    print(answer)
    print("----------------------\n")
