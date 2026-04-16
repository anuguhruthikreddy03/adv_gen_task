from langchain.prompts import PromptTemplate

extract_prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
Extract only:
1. Skills
2. Experience
3. Tools

Resume:
{resume}
"""
)

match_prompt = PromptTemplate(
    input_variables=["skills", "jd"],
    template="""
Compare candidate skills with job description.

Candidate Skills:
{skills}

Job Description:
{jd}

Give:
Matched Skills
Missing Skills
Match Percentage
"""
)

score_prompt = PromptTemplate(
    input_variables=["match_result"],
    template="""
Based on the following match result, assign score out of 100.

{match_result}

Also explain why score was given.
"""
)