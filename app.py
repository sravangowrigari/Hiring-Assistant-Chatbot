import streamlit as st
from model import generate_question_list

st.set_page_config(page_title="TalentScout Hiring Assistant")

# ---------- Session State ----------
if "step" not in st.session_state:
    st.session_state.step = 1

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I’m TalentScout’s Hiring Assistant.\n\n"
                "I’ll ask you a few questions to understand your background "
                "and technical skills.\n\n"
                "You can type **exit** at any time to end the conversation.\n\n"
                "Let’s get started — what is your **full name**?"
            )
        }
    ]

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

# ---------- UI ----------
st.title("🤖 TalentScout Hiring Assistant")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Helpers ----------
def is_exit(text):
    return text.lower() in ["exit", "quit", "bye", "stop"]

def is_valid_tech_stack(text):
    if len(text.strip()) < 3:
        return False
    if all(char.isdigit() or char in ", " for char in text):
        return False
    return True

# ---------- Input ----------
user_input = st.chat_input("Type your response here...")

if user_input:

    # GLOBAL FALLBACK
    if user_input.strip() == "":
        st.session_state.messages.append({
            "role": "assistant",
            "content": "I didn’t catch that. Could you please enter a valid response?"
        })
        st.rerun()

    # EXIT
    if is_exit(user_input):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Thank you for your time. Our recruitment team will contact you shortly. Have a great day!"
        })
        st.stop()

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # ---------- Conversation Flow ----------
    if st.session_state.step == 1:
        st.session_state.profile["name"] = user_input
        response = "Please provide your email address."
        st.session_state.step += 1

    elif st.session_state.step == 2:
        st.session_state.profile["email"] = user_input
        response = "What is your phone number?"
        st.session_state.step += 1

    elif st.session_state.step == 3:
        st.session_state.profile["phone"] = user_input
        response = "How many years of professional experience do you have?"
        st.session_state.step += 1

    elif st.session_state.step == 4:
        st.session_state.profile["experience"] = user_input
        response = "Which position(s) are you applying for?"
        st.session_state.step += 1

    elif st.session_state.step == 5:
        st.session_state.profile["role"] = user_input
        response = "What is your current location?"
        st.session_state.step += 1

    elif st.session_state.step == 6:
        st.session_state.profile["location"] = user_input
        response = "Please list your tech stack (comma separated)."
        st.session_state.step += 1

    elif st.session_state.step == 7:
        if not is_valid_tech_stack(user_input):
            response = (
                "I didn’t quite understand that 🤔\n\n"
                "Please list your tech stack clearly, for example:\n"
                "**Python, SQL, Power BI**"
            )
        else:
            tech_stack = [t.strip() for t in user_input.split(",")]
            st.session_state.profile["tech_stack"] = tech_stack

            # Generate questions ONCE
            st.session_state.questions = generate_question_list(
                tech_stack,
                st.session_state.profile["experience"]
            )

            st.session_state.current_q = 0
            st.session_state.step = 8

            response = (
                f"Technical Question 1:\n\n"
                f"{st.session_state.questions[0]}"
            )

    elif st.session_state.step == 8:
        # Store answer
        st.session_state.answers.append({
            "question": st.session_state.questions[st.session_state.current_q],
            "answer": user_input
        })

        st.session_state.current_q += 1

        if st.session_state.current_q < len(st.session_state.questions):
            response = (
                f"Technical Question {st.session_state.current_q + 1}:\n\n"
                f"{st.session_state.questions[st.session_state.current_q]}"
            )
        else:
            st.session_state.step = 9
            response = (
                "✅ Thank you for answering the technical questions.\n\n"
                "Our recruitment team will review your responses and contact you soon."
            )

    else:
        response = "Screening completed."

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()
