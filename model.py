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
    prompt = f"""
You are a senior technical interviewer.

Candidate experience: {experience} years
Technologies: {", ".join(tech_stack)}

INSTRUCTIONS:
- Generate technical interview questions
- Focus on practical, real-world usage
- Do NOT include answers
- Return a numbered list only
"""

    response = llm(prompt)
    raw_text = response[0]["generated_text"]

    questions = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            questions.append(line.split(".", 1)[-1].strip())

    # ✅ SMART FALLBACK (guarantee up to 5 questions)
    if len(questions) < 5:
        fallback_pool = []
        for tech in tech_stack:
            fallback_pool.extend([
                f"Explain a real-world use case where you used {tech}.",
                f"What are common challenges you faced while working with {tech}?",
                f"How do you optimize performance when using {tech}?"
            ])

        for q in fallback_pool:
            if len(questions) >= 5:
                break
            if q not in questions:
                questions.append(q)

    return questions[:5]

