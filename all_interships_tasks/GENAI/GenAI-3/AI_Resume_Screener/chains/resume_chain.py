from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from prompts.prompts import extract_prompt, match_prompt, score_prompt

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

parser = StrOutputParser()

extract_chain = extract_prompt | llm | parser
match_chain = match_prompt | llm | parser
score_chain = score_prompt | llm | parser