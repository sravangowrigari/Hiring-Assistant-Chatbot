from transformers import pipeline

llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_new_tokens=400
)

SYSTEM_PROMPT = """
You are an intelligent Hiring Assistant.
Generate technical interview questions only.
Do NOT provide answers.
"""

def generate_technical_questions(tech_stack, experience):
    prompt = f"""
Candidate experience: {experience} years
Tech stack: {", ".join(tech_stack)}

Generate 3-5 technical interview questions for each technology.
"""

    response = llm(prompt)
    return response[0]["generated_text"]
