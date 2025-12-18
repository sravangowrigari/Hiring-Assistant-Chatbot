import streamlit as st
from transformers import pipeline
from huggingface_hub import login
import os

# 🔐 Login to Hugging Face (token required for LLaMA models)
# Set HF_TOKEN as env variable or Streamlit secret
login(token=os.environ.get("HF_TOKEN"))

# Load model once (VERY important for Streamlit Cloud)
@st.cache_resource
def load_model():
    return pipeline(
        task="text-generation",
        model="meta-llama/Llama-3.2-1B",
        max_new_tokens=250,
        do_sample=False,
        temperature=0.3
    )

llm = load_model()


def generate_question_list(tech_stack, experience):
    """
    Generate up to 5 technical interview questions
    strictly based on the provided tech stack.
    """

    prompt = f"""
You are a technical interviewer.

Candidate experience: {experience} years
Tech stack: {", ".join(tech_stack)}

INSTRUCTIONS:
- Generate a MAXIMUM of 5 technical interview questions TOTAL
- Questions must be strictly related to the given tech stack
- Focus on practical, real-world usage
- Do NOT include answers
- Do NOT include explanations
- Do NOT repeat questions
- Output ONLY a numbered list

Example:
1. Question
2. Question
"""

    response = llm(prompt)
    raw_text = response[0]["generated_text"]

    # -------- Parse questions safely --------
    questions = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            questions.append(line.split(".", 1)[-1].strip())

    # -------- Guaranteed fallback (never empty) --------
    if len(questions) < 5:
        fallback_pool = []
        for tech in tech_stack:
            fallback_pool.extend([
                f"Explain a real-world use case where you used {tech}.",
                f"What challenges have you faced while working with {tech}?",
                f"How do you optimize performance when using {tech}?"
            ])

        for q in fallback_pool:
            if len(questions) >= 5:
                break
            if q not in questions:
                questions.append(q)

    return questions[:5]
