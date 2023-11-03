import setup_env
import logging
from src.model_loader import ModelLoader
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from transformers import pipeline,  AutoTokenizer, AutoModelForSeq2SeqLM

model_loader = ModelLoader()
model_loader.download_models_pretrained()

directory = model_loader.models['flan-t5-large']['directory']
model_id = model_loader.models['flan-t5-large']['id']
logging.info(f"Loading {model_id} from {directory}")
tokenizer = AutoTokenizer.from_pretrained(directory)
model = AutoModelForSeq2SeqLM.from_pretrained(directory)
logging.info(f"{model_id} loaded")

pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=100
)


template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
logging.info(f"Prompting: {prompt}")

llm = HuggingFacePipeline(pipeline=pipe)
llm_chain = LLMChain(
    prompt=prompt,
    llm=llm
)

print(llm_chain.run("What is the capital of Israel?"))
