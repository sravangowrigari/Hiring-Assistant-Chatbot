from transformers import pipeline
import streamlit as st

# Cache model so it loads only once
@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-large",
        max_new_tokens=350
    )

llm = load_model()

def generate_question_list(tech_stack, experience):
    """
    Generates up to 5 high-quality, tech-specific interview questions.
    """

    prompt = f"""
You are a senior technical interviewer.

Candidate experience: {experience} years
Technologies: {", ".join(tech_stack)}

INSTRUCTIONS:
- Generate a MAXIMUM of 5 technical interview questions TOTAL
- Questions MUST be strictly related to the given technologies
- Mix questions across technologies
- Questions should test practical, real-world understanding
- Do NOT include answers or explanations
- Do NOT repeat questions
- Output ONLY a numbered list

Example:
1. Question
2. Question
"""

    response = llm(prompt)
    raw_text = response[0]["generated_text"]

    questions = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            questions.append(line.split(".", 1)[-1].strip())

    # 🔐 HARD FALLBACK (never crash)
    if not questions:
        for tech in tech_stack:
            questions.append(
                f"Explain a real-world use case where you used {tech}."
            )

    return questions[:5]
