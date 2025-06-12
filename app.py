import os
import google.generativeai as genai
import streamlit as st
import json

# Configure Gemini API
genai.configure(api_key="AIzaSyABRssRHY3TvWV9WCxb8KonfLvmars1qB8")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="""
    - Start the conversation with:  
      "Hi! I'm your personal assistant Ria 2.0! I'll help you find the best SBI Life policy just by asking a few questions!"  

    - If the user doesn't provide details, ask these questions one by one:  
      1. What is your age?  
      2. Do you have any health concerns? If yes, specify.  
      3. Are you married? (Yes/No)  
      4. Do you have children? (Yes/No)  
      5. What is your risk preference? (Low, Medium, High)?  

    - Once all details are collected, suggest any one of these policies:
        SBI Life - Smart Swadhan Supreme
        SBI Life - Saral Swadhan Supreme
        SBI Life - eShield Next
        SBI Life - eWealth Insurance Online Plan
        SBI Life - Retire Smart
        SBI Life - Smart Platina Plus
        SBI Life - Smart Annuity Plus
        SBI Life - Smart Platina Assure
        SBI Life - Saral Jeevan Bima
        SBI Life - Sampoorna Cancer Suraksha
        SBI Life - Smart Wealth Builder
        SBI Life - Smart InsureWealth Plus
        SBI Life - Smart Champ
        SBI Life - Retire Smart Plus
        SBI Life - New Smart Samriddhi

    - Present the recommendations in a friendly and conversational way. Example:  
      *"Based on your inputs, I recommend the following policies: [Policy Names]. These options align with your financial needs and risk preference. Would you like to learn more?"*  

    - Keep responses under 200 words.
    """,
)

# Initialize chat session in Streamlit session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Custom CSS for layout
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #e60143, #3f287a);
        color: #ffffff;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.2);
        color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        animation: fadeIn 0.5s ease-in-out;
    }
    .stChatMessage.user {
        background-color: rgba(255, 255, 255, 0.3);
    }
    .stChatMessage.model {
        background-color: rgba(255, 255, 255, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar (Left Section) for About & Policies
with st.sidebar:
    st.image("https://th.bing.com/th/id/OIP.IvoUo0h_QMzaLbg5xd_uuwHaEK?w=322&h=180&c=7&r=0&o=5&pid=1.7", width=100)

    st.markdown("## About:")
    st.markdown(
        "This is a prototype chatbot that provides personalized support to find the best SBI Life policy based on just a few questions."
    )
    st.markdown("- Developed by Team Hackslayers")
    
    st.markdown("## Available SBI Life Policies")
    policies = [
        "SBI Life - Smart Swadhan Supreme Brochure",
        "SBI Life - Saral Swadhan Supreme Brochure",
        "SBI Life - eShield Next Brochure",
        "SBI Life - eWealth Insurance Online Plan",
        "SBI Life - Retire Smart",
        "SBI Life - Smart Platina Plus",
        "SBI Life - Smart Annuity Plus",
        "SBI Life - Smart Platina Assure",
        "SBI Life - Saral Jeevan Bima",
        "SBI Life - Sampoorna Cancer Suraksha",
        "SBI Life - Smart Wealth Builder",
        "SBI Life - Smart InsureWealth Plus",
        "SBI Life - Smart Champ",
        "SBI Life - Retire Smart Plus",
        "SBI Life - New Smart Samriddhi"
    ]
    for policy in policies:
        st.markdown(f"- {policy}")

    # Reset Chat Button
    if st.button("Reset Chat"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# Main Section - Chatbot
st.title("🤖 SBI Life Policy Chatbot")
st.write("Hi! I'm your personal assistant Ria 2.0! I'll help you find the best SBI Life policy by asking a few questions.")

# Chat history container
chat_history_container = st.container()

with chat_history_container:
    for message in st.session_state.chat_session.history:
        if isinstance(message, dict):
            role = message.get("role", "assistant")
            parts = message.get("parts", [])
            content = parts[0]["text"] if parts and isinstance(parts[0], dict) and "text" in parts[0] else str(parts[0])
            with st.chat_message(role):
                st.write(content)

# Chat input
user_input = st.chat_input("Type your response here...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    response = st.session_state.chat_session.send_message(user_input)

    try:
        bot_response_json = json.loads(response.text)
        bot_response = bot_response_json.get("response", response.text)
    except (json.JSONDecodeError, AttributeError):
        bot_response = response.text if hasattr(response, "text") else str(response)
    
    st.session_state.chat_session.history.append({"role": "user", "parts": [{"text": user_input}]})
    st.session_state.chat_session.history.append({"role": "assistant", "parts": [{"text": bot_response}]})

    with st.chat_message("assistant"):
        st.write(bot_response)

    # Feedback Mechanism
    if "recommendation" in bot_response.lower():
        feedback = st.radio("Was this recommendation helpful?", ("Yes", "No"))
        if feedback:
            st.write("Thank you for your feedback!")
