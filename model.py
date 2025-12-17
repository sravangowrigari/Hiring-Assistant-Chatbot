from transformers import pipeline

# Lightweight model for Streamlit Cloud
llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_new_tokens=300
)

def generate_question_list(tech_stack, experience):
    """
    Generate a bounded list of technical questions
    based on the given tech stack.
    """

    prompt = f"""
You are a technical interviewer.

Candidate experience: {experience} years
Technologies: {", ".join(tech_stack)}

TASK:
- Generate a MAXIMUM of 5 technical interview questions TOTAL
- Questions must be strictly related to the listed technologies
- Mix questions across technologies
- Do NOT include explanations or answers
- Do NOT repeat questions
- Return ONLY a numbered list

Example:
1. Question
2. Question
"""

    response = llm(prompt)
    raw_text = response[0]["generated_text"]

    # Clean & extract questions safely
    questions = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            questions.append(line.split(".", 1)[-1].strip())

    return questions[:5]
