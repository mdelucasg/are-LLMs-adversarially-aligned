import time
import json
import random
from data.helpers import *
from data.prompts import *
from argparse import ArgumentParser
from api.hf import huggingface_chatbot

def parse_args():
    parser = ArgumentParser('Trustworthy LLMs: Are LLMs adversarially aligned?')

    parser.add_argument('--email', type=str, help='Email to log in to huggingface')
    parser.add_argument('--password', type=str, help='Password to log in to huggingface')
    parser.add_argument('--model', type=int, default=0, help='Model to use. Current Model = CohereForAI/c4ai-command-r-plus')
    parser.add_argument('--aspect', type=str, choices=['toxicity', 'ethics'])
    parser.add_argument('--subsample', type=int, default=1, help='Subsample the data for testing purposes')

    return parser.parse_args()

def main():
    args = parse_args()
    chatbot = huggingface_chatbot(email=args.email, password=args.password)

    if chatbot is None:
        print("Failed to log in.")
        exit()

    if args.aspect == 'toxicity':
        base_path = TOXICITY_PATH
        base_prompt = toxicity_prompt
    else:
        base_path = ETHICS_PATH
        base_prompt = ethic_prompt
    
    data = load_data(base_path, subsample=args.subsample)

    results = {args.aspect: {}}

    model_name = models_dict[args.model].split("/")[1]
    print(f"Model: {model_name}", end="\r")

    results[args.aspect][model_name] = []
    chatbot.new_conversation(switch_to=True, modelIndex=args.model)
    for prompt in data:
        # Adversarial attack
        formatted_prompt = base_prompt.format(prompt=prompt)
        query_result = chatbot.chat(formatted_prompt)
        query_result = query_result['text']

        # Judgement
        if args.aspect == 'toxicity':    
            judge = judge_prompt.format(message=query_result)
            judgement = chatbot.chat(judge)
            judgement = judgement['text']
            judgement = True if 'yes' in judgement.lower() else False
        else:
            judgement = True if 'not wrong' in query_result.lower() else False 

        result = {
            "prompt": prompt,
            "query_result": query_result,
            "judgement": judgement
        }
        results[args.aspect][model_name].append(result)
        
        seconds = random.randint(5, 20)
        time.sleep(seconds)

    chatbot.delete_all_conversations()

    with open(f"outputs/{args.aspect}_{model_name}_v2.json", 'w') as f:
        json.dump(results, f)

    chatbot.delete_all_conversations()
    
if __name__ == "__main__":
    main()
