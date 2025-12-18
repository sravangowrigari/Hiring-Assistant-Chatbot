import streamlit as st
from transformers import pipeline
from huggingface_hub import login
import os

login(token=os.environ.get("HF_TOKEN"))

# Cache model to avoid reload on every rerun
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="meta-llama/Llama-3.2-3B-Instruct",
        torch_dtype="auto",
        device_map="auto",
        max_new_tokens=300
    )

llm = load_model()

def generate_question_list(tech_stack, experience):
    """
    Generate up to 5 high-quality, tech-specific interview questions.
    """

    prompt = f"""
You are a senior technical interviewer.

Candidate experience: {experience} years
Technologies: {", ".join(tech_stack)}

INSTRUCTIONS:
- Generate a MAXIMUM of 5 technical interview questions TOTAL
- Questions MUST be strictly related to the given technologies
- Mix questions across technologies
- Focus on practical, real-world usage
- Do NOT include answers or explanations
- Do NOT repeat questions
- Output ONLY a numbered list

Example:
1. Question
2. Question
"""

    response = llm(
        prompt,
        do_sample=False,   # deterministic output
        temperature=0.3
    )

    raw_text = response[0]["generated_text"]

    # Extract questions safely
    questions = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            questions.append(line.split(".", 1)[-1].strip())

    # 🔐 GUARANTEED FALLBACK (never crash, never < tech count)
    if len(questions) < 5:
        fallback_pool = []
        for tech in tech_stack:
            fallback_pool.extend([
                f"Explain a real-world use case where you used {tech}.",
                f"What are common challenges you faced while working with {tech}?",
                f"How do you optimize performance when working with {tech}?"
            ])

        for q in fallback_pool:
            if len(questions) >= 5:
                break
            if q not in questions:
                questions.append(q)

    return questions[:5]
