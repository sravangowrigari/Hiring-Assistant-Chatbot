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
You are a technical interviewer.

Candidate experience: {experience} years  
Technologies: {", ".join(tech_stack)}

STRICT INSTRUCTIONS:
- For EACH technology, generate EXACTLY 3 technical interview questions
- Questions MUST be directly related to that technology
- Do NOT ask HR or behavioral questions
- Do NOT provide answers
- Format exactly like this:

<TECHNOLOGY NAME>
1. Question
2. Question
3. Question

Begin now.
"""

    response = llm(prompt)
    return response[0]["generated_text"].strip()
