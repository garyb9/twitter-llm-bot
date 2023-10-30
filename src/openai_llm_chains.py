import random
from typing import List, Any
from openai_client import llm
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm_chains = {
    "quote_tweets": [
        LLMChain(
            prompt=PromptTemplate(
                template="""Generate 10 tweets of quotes by {name}, no hashtags.""", input_variables=["name"]
            ),
            llm=llm
        ),
        LLMChain(
            prompt=PromptTemplate(
                template="""Generate 10 tweets of quotes by {name}, no hashtags, format each tweet as 2-3 lines, end with name.""", input_variables=["name"]
            ),
            llm=llm
        ),
    ],
    "philosophical_tweets": [
        LLMChain(
            prompt=PromptTemplate(
                template="""Generate 10 tweets about {topic} with a philosophical sense, without hashtags and emojis.""", input_variables=["topic"]
            ),
            llm=llm
        ),
    ]
}


def run_random_tweet(group: str, input_variables: List[str]) -> Any:
    response = random.choice(llm_chains[group]).run(input_variables)
    return response


# Random example
# print(run_random_tweet("quote_tweets", ["Max Stirner"]))
