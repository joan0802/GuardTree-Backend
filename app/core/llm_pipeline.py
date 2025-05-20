from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM, TextStreamer
"""
Setup the LLM pipeline using Hugging Face Transformers
"""
model_name = "Qwen/Qwen1.5-7B-Chat"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    use_safetensors=True,
)
streamer = TextStreamer(tokenizer, skip_prompt=True)

llm_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    use_cache=True,
    device_map="auto",
    max_length=32768,
    do_sample=True,
    top_k=5,
    num_return_sequences=1,
    streamer=streamer,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id,
)
