from chains.resume_chain import extract_chain, match_chain, score_chain

from sample_data import resume1, resume2, resume3, job_description

def evaluate_resume(resume):
    print("\n========== NEW CANDIDATE ==========\n")

    extracted = extract_chain.invoke({"resume": resume})
    print("EXTRACTED:\n", extracted)

    matched = match_chain.invoke({
        "skills": extracted,
        "jd": job_description
    })
    print("\nMATCH RESULT:\n", matched)

    final = score_chain.invoke({
        "match_result": matched
    })
    print("\nFINAL SCORE:\n", final)

# Run all 3 resumes
evaluate_resume(resume1)
evaluate_resume(resume2)
evaluate_resume(resume3)