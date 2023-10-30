from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain import OpenAIAPI


def generate_tweet(prompt, model_name, max_length=280):
    # Load the Hugging Face model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Generate a tweet using Langchain
    api = OpenAIAPI()
    tweet = api.compose(text=prompt, models=[model])

    # Ensure the tweet is not longer than the specified length
    tweet = tweet[:max_length]

    return tweet
