from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json
import pandas as pd 
from dotenv import load_dotenv
load_dotenv()
from src.response import *
from src.logger import logging
from src.utils import read_file, get_table_data

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# print(GOOGLE_API_KEY)


llm = ChatGoogleGenerativeAI(model="gemini-pro")

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
You only have to relpy the string (i.e : not start with  RESPONSE_JSON =)
"""
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
    )
quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE2)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain],
                                        input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)

# NUMBER=15
# SUBJECT="data science"
# TONE="simple"

# with open('document.txt','r') as f:
#     TEXT = f.read()
# response=generate_evaluate_chain.invoke(
#         {
#             "text": TEXT,
#             "number": NUMBER,
#             "subject":SUBJECT,
#             "tone": TONE,
#             "response_json": json.dumps(RESPONSE_JSON)
#         }
#         )

# print(response.get('quiz'))
# print('_#-#'*50)
# print(response.get('review'))
