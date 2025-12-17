import streamlit as st
from model import generate_technical_questions

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



# ---------- UI ----------
st.title("🤖 TalentScout Hiring Assistant")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def is_valid_tech_stack(text):
    # Reject empty, numbers only, or symbols
    if len(text.strip()) < 3:
        return False
    if all(char.isdigit() or char in ", " for char in text):
        return False
    return True

# Exit keywords
def is_exit(text):
    return text.lower() in ["exit", "quit", "bye", "stop"]

user_input = st.chat_input("Type your response here...")

if user_input.strip() == "":
    st.session_state.messages.append({
        "role": "assistant",
        "content": "I didn’t catch that. Could you please enter a valid response?"
    })
    st.rerun()

if user_input:
    if is_exit(user_input):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Thank you for your time. Our recruitment team will contact you shortly. Have a great day!"
        })
        st.stop()

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # ---------- Conversation Flow ----------
    if st.session_state.step == 0:
        response = "Hello! I’m TalentScout’s Hiring Assistant. What is your full name?"
        st.session_state.step += 1

    elif st.session_state.step == 1:
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
                "**Python, SQL, Power BI, Django**"
            )
            else:
                tech_stack = [t.strip() for t in user_input.split(",")]
                st.session_state.profile["tech_stack"] = tech_stack
        
                response = "Thank you. Here are your technical screening questions:\n\n"
                questions = generate_technical_questions(
                    tech_stack,
                    st.session_state.profile["experience"]
                )
        
                response += questions
                st.session_state.step += 1


    else:
        response = "Screening completed. Thank you for your participation."

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()
