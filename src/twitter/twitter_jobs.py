from langchain.llms import OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer


def get_tweets_job():
    pass  # TODO:


def post_tweet_job():
    pass  # TODO:


def create_tweet_job():
    pass  # TODO:


def generate_tweet(prompt, model_name, max_length=280):
    # Load the Hugging Face model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Generate a tweet using Langchain
    api = OpenAI()
    tweet = api.compose(text=prompt, models=[model])

    # Ensure the tweet is not longer than the specified length
    tweet = tweet[:max_length]

    return tweet
