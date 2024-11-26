import openai
import streamlit as st

# OpenAI API setup
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = "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"

# Virtual Assistant system instructions
system_instructions = [
    {
        "role": "system",
        "content": (
            "You are Kalai Safaris Virtual Assistant, a helpful assistant for Kalai Safaris. "
            "Kalai Safaris is a destination management company offering Zambezi River cruises above the Victoria Falls. "
            "Your goal is to assist customers with information about our cruises, events, pricing, and booking options."
        ),
    },
    {
        "role": "system",
        "content": (
            "Kalai Safaris Overview:\n"
            "- Kalai Safaris is a boating safari company located above the Victoria Falls. We offer a 40-seater and a 10-seater cruise vessel. "
            "Our services include tailored safari cruises, event hosting, and travel packages."
        ),
    },
    {
        "role": "system",
        "content": (
            "Cruise Types:\n"
            "1. Sunrise Cruise: A 2-hour early morning cruise (06:00 am to 08:00 am) showcasing nature and wildlife as the day begins.\n"
            "2. Lunch Time Cruise: A 2-hour afternoon cruise (12:00 pm to 02:00 pm) featuring a calm experience with optional meals.\n"
            "3. Sunset Cruise: A 2-hour late afternoon cruise (04:00 pm to sunset) with opportunities to see wildlife and breathtaking sunsets."
        ),
    },
    {
        "role": "system",
        "content": (
            "Event Hosting:\n"
            "- Host conferences, weddings, cocktails, or outdoor functions at our riverside jetty with the Zambezi River as a backdrop."
        ),
    },
    {
        "role": "system",
        "content": (
            "Cruise Pricing:\n"
            "- $10.00 per person for an affordable cruise.\n"
            "- $20.00 per person for a school special package (with a cash bar).\n"
            "- $40.00 per person for a lunch cruise with meals and beverages.\n"
            "- $50.00 per person for a dinner cruise (excludes Parks river usage fee)."
        ),
    },
    {
        "role": "system",
        "content": (
            "Future Plans:\n"
            "- Automating client engagement and implementing a payment gateway (e.g., PayNow) to streamline bookings.\n"
            "- Introducing the Gold Package: Includes an overnight stay for an additional $50.\n"
            "- Preparing for the 2025 festive period with automated solutions and special packages."
        ),
    },
    {
        "role": "system",
        "content": (
            "Contact Information:\n"
            "- Address: Riverside Jetty, next to Palm Lodge, Victoria Falls, Zimbabwe.\n"
            "- Phone: +263772212184\n"
            "- Email: reservation@kalaisafaris.com"
        ),
    },
]


# Set page configuration for title and layout
st.set_page_config(page_title="Kalai Safaris Virtual Assistant Chat", page_icon="logo.png", layout="centered")

# Custom styling for chat UI
st.markdown(""" 
    <style>
    body {
        background-color: #f0f2f6;
    }
    .chat-message {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #d1e7dd;
        text-align: left;
        display: inline-block;
        color: #000;
    }
    .ai-message {
        background-color: #f8d7da;
        text-align: left;
        display: inline-block;
        color: #000;
        margin-right:25%;
    }
    </style>
""", unsafe_allow_html=True)

# Function to calculate dynamic margin-left based on the length of the user message
def calculate_margin(user_input):
    length = len(user_input)
    if length < 10:
        return "80%"  # Short message
    elif length < 50:
        return "60%"  # Medium message
    else:
        return "40%"  # Longer message

# Chatbot functionality
def chatbot():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display the chat history
    for chat in st.session_state.chat_history:

        if chat['role'] == 'user':
            margin_left = calculate_margin(chat['content'])  # Calculate margin-left based on message length
            st.markdown(
                f"<div class='chat-message user-message' style='margin-left: {margin_left};'><b>You:</b> {chat['content']}</div>", 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='chat-message ai-message'><b>Kalai Safaris Virtual Assistant:</b> {chat['content']}</div>", 
                unsafe_allow_html=True
            )

    st.markdown("---")

    question = st.text_input("", placeholder="Talk to Kalai Safaris Virtual Assistant here...")
    if st.button("Send"):
        if question:
            st.session_state.chat_history.append({"role": "user", "content": question})

            messages = system_instructions + [{"role": "user", "content": question}]
            reply = ""
            # OpenAI API call
            with st.spinner("Processing ...."):
                try:
                    response = openai.ChatCompletion.create(
                      model="openai/gpt-3.5-turbo",
                      messages=messages,
                    )
                    reply = response.choices[0].message['content']
                except Exception as e:
                    reply = (e+" Error communicating with Kalai Safaris Virtual Assistant. Please try again later.")

            answer = reply
            st.session_state.chat_history.append({"role": "ai", "content": answer})
            
            st.rerun()

# Main chatbot interface
st.title("Kalai Safaris Virtual Assistant ")
st.write("Hello! I am the virtual assistant for Kalai Safaris, how can I assist you?")
chatbot()
