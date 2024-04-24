import os
import jsonlines

ETHICS_PATH = 'data/ethics'
TOXICITY_PATH = 'data/toxicity'

models_dict = {
    0: 'CohereForAI/c4ai-command-r-plus',
    1: 'HuggingFaceH4/zephyr-orpo-141b-A35b-v0.1',
    2: 'mistralai/Mixtral-8x7B-Instruct-v0.1',
    3: 'google/gemma-1.1-7b-it',
    4: 'NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO',
    5: 'mistralai/Mistral-7B-Instruct-v0.2'
}

def load_data(base_path = TOXICITY_PATH):
    data = []
    for filename in os.listdir(base_path):
        if filename.endswith(".jsonl"):
            path = os.path.join(os.getcwd(), base_path, filename)
            with jsonlines.open(path) as reader:
                for obj in reader:
                    prompt = obj["prompt"]["text"]
                    data.append(prompt)

    return data