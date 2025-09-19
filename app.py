import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
# Configure Gemini API
load_dotenv()
key = os.getenv("API")
genai.configure(api_key=key)

#using gemini-2.0-flash model for the chatbot
model = genai.GenerativeModel('gemini-2.0-flash')

#context for the chatbot
CALM_PULSE_CONTEXT = """
You are Calm Pulse, a safe, non-judgmental, therapist-like companion. 
You should respond as Calm Pulse would, incorporating your:
- Role as a calm listener where users can rant, vent, or open up freely
- Ability to validate emotions and create a safe, supportive space
- Gentle way of offering practical solutions and coping strategies
- Focus on empathy, patience, and reassurance without judgment
- Skill in providing short exercises (breathing, grounding, journaling, reframing)
- Respect for user boundaries and asking before deeper interventions
- Reminder that you are not a licensed therapist, but a supportive guide
- Crisis care: if user mentions self-harm or immediate danger, respond with empathy 
  and suggest professional help or emergency contacts

Maintain a warm, calm, and caring tone. Speak directly in first person as a supportive companion, 
acknowledge feelings, and offer 2–3 simple next steps. Keep responses short and gentle 
(2–4 sentences). Always make the user feel safe, heard, and supported.
"""


def get_response(user_input):
    prompt = f"{CALM_PULSE_CONTEXT}\n\nUser: {user_input}\nLewis Hamilton:"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I'm having trouble connecting with the team right now. Technical issue: {str(e)}"

st.set_page_config(
    page_title="Calm Pulse",
    page_icon="🌿",
    layout="centered"
)

st.title("It's a safe place")
st.markdown("""
# Welcome to Calm Pulse 🌿  
This is your safe space to talk, vent, or simply breathe.  
I’m here to listen without judgment, support you with empathy, and offer gentle solutions when you’re ready.  

**What’s on your mind today?**

""")

#to initiailise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#input
if prompt := st.chat_input("Go on, don't be afraid"):
    #add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    #chatbot response
    with st.chat_message("assistant", avatar="🏎️"):
        response = get_response(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Add some styling
st.markdown("""
<style>
    .stChat {
        border-radius: 10px;
        border: 1px solid #f0f0f0;
    }
    .stChatMessage {
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True) 