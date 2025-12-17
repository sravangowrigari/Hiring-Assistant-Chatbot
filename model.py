from transformers import pipeline

# Load instruction-tuned Hugging Face model
# Note: This model can run on CPU, GPU is optional
llm = pipeline(
    "text-generation",
    model="mistralai/Mistral-7B-Instruct-v0.2",
    device_map="auto",
    max_new_tokens=600
)

SYSTEM_PROMPT = """
You are an intelligent Hiring Assistant for TalentScout.
Your task is to generate technical interview questions only.
Do NOT provide answers.
Be concise, professional, and role-focused.
"""

def generate_technical_questions(tech_stack, experience):
    """
    Generates technical questions based on tech stack and experience.
    """
    prompt = f"""
{SYSTEM_PROMPT}

Candidate experience: {experience} years
Tech stack: {", ".join(tech_stack)}

Generate 3–5 open-ended technical interview questions
for each technology listed.
"""

    response = llm(
        prompt,
        temperature=0.4,
        top_p=0.9,
        do_sample=True
    )

    return response[0]["generated_text"].strip()
