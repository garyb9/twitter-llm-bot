import json
import random
from typing import List, Any
from llm.openai import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def generate_prompt(seed_idea, temperature=0.7, max_tokens=100, num_completions=1):
    """
    Generates prompts based on a seed idea using OpenAI's API through LangChain.

    Parameters:
    - seed_idea: A string containing the initial idea or seed for the prompt.
    - temperature: A float that controls the randomness of the output. Higher values mean more creative responses.
    - max_tokens: The maximum number of tokens to generate in the output.
    - num_completions: The number of completions to generate for the given prompt.

    Returns:
    A list of generated prompts based on the input seed idea.
    """
    prompts = []
    for _ in range(num_completions):
        response = openai.generate(seed_idea,
                                   temperature=temperature,
                                   max_tokens=max_tokens,
                                   num_completions=1)  # Adjust according to your needs
        prompts.append(response)
    return prompts


def generate_prompt_from_json(input_json, temperature=0.7, max_tokens=100, num_chains=1):
    """
    Generates prompts based on a JSON list of dictionaries, each containing 'role' and 'prompt' keys.

    Parameters:
    - input_json: A JSON string representing a list of dictionaries. Each dictionary should have
                  'role' and 'prompt' keys.
                  Example format: '[{"role": "role1", "prompt": "prompt1"}, {"role": "role2", "prompt": "prompt2"}]'
    - temperature: A float controlling the randomness of the output. Higher values mean more creative responses.
    - max_tokens: The maximum number of tokens to generate for each prompt in the chain.
    - num_chains: The number of chained prompts to generate from the input list.

    Returns:
    A list of generated prompts, each influenced by the preceding output in the chain.
    """
    # Parse the JSON string into a Python list
    prompt_list = json.loads(input_json)

    chained_prompts = []
    for _ in range(num_chains):
        current_text = ""
        for item in prompt_list:
            role = item['role']
            seed_idea = item['prompt']
            prompt_text = f"{role}: {seed_idea}\n{current_text}"
            response = openai.generate(prompt_text,
                                       temperature=temperature,
                                       max_tokens=max_tokens,
                                       num_completions=1)  # Adjust according to your needs
            # Append the generated text to the current text to chain the next prompt
            current_text += "\n" + response + "\n"
        chained_prompts.append(current_text.strip())
    return chained_prompts


# llm_chains = {
#     "quote_tweets": [
#         LLMChain(
#             prompt=PromptTemplate(
#                 template="""Generate 10 tweets of quotes by {name}, no hashtags.""", input_variables=["name"]
#             ),
#             llm=openai
#         ),
#         LLMChain(
#             prompt=PromptTemplate(
#                 template="""Generate 10 tweets of quotes by {name}, no hashtags, format each tweet as 2-3 lines, end with name.""", input_variables=["name"]
#             ),
#             llm=openai
#         ),
#     ],
#     "philosophical_tweets": [
#         LLMChain(
#             prompt=PromptTemplate(
#                 template="""Generate 10 tweets about {topic} with a philosophical sense, without hashtags and emojis.""", input_variables=["topic"]
#             ),
#             llm=openai
#         ),
#     ]
# }


# def run_random_tweet(group: str, input_variables: List[str]) -> Any:
#     response = random.choice(llm_chains[group]).run(input_variables)
#     return response


# Random example
# print(run_random_tweet("quote_tweets", ["Max Stirner"]))
