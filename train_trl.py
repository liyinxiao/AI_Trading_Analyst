from datasets import Dataset
from trl import GRPOTrainer
from trl import GRPOConfig, GRPOTrainer
import torch
import re
import json
from training_data_dummy import training_data
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load dummy training data
dataset = Dataset.from_list([{"prompt": x[0], "answer": x[1]} for x in training_data])

training_args = GRPOConfig(
    output_dir="qwen-GRPO",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    num_train_epochs=1,


    
    logging_steps=1,
)


def extract_rating(response):
    print("raw response: ", response)
    json_str = (
        re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        data = json.loads(json_str)
        rating = data.get("rating", "unavailable").lower()
        return rating
    except:
        if '"rating": "strong buy"' in response:
            return "strong buy"
        if '"rating": "strong sell"' in response:
            return "strong sell"
        if '"rating": "hold"' in response:
            return "hold"
        if '"rating": "buy"' in response:
            return "buy"
        if '"rating": "sell"' in response:
            return "sell"
        return "unavailable"


def get_rating_score(rating, label):
    d = {
        "strong buy": 2,
        "buy": 1,
        "hold": 0,
        "sell": -1,
        "strong sell": -2,
    }
    diff = abs(d.get(rating.lower(), 10) - d[label])
    return -min(diff, 2)


def reward_func(prompts, completions, answer, **kwargs) -> list[float]:
    """
    Reward function that checks how accurate the rating is compared with ground-truth label
    """

    extracted_responses = [extract_rating(c) for c in completions]
    results = [get_rating_score(x, y) for x, y in zip(extracted_responses, answer)]
    print("scores: ", results)
    return results


tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B")

trainer = GRPOTrainer(
    model="Qwen/Qwen3-0.6B",
    processing_class=tokenizer,
    reward_funcs=reward_func,
    train_dataset=dataset,
    args=training_args,
)

trainer.train()
