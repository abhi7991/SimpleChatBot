# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 22:08:50 2024
strea
@author: abhis
"""

import os
import streamlit as st
import openai

from dotenv import load_dotenv
load_dotenv()

# Get OpenAI API key from environment
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Configure Streamlit page settings
st.set_page_config(
    page_title="MovieMatch",
    page_icon="🎬",
    layout="centered"
)

# Initialize chat session if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("🎬 MovieMatch - Your Personal Movie Guide")

# Load and display images from local repository
image_dir = os.getcwd()+"\someImages"  # Directory where your images are stored
images = os.listdir(image_dir)

# Display images in a sidebar
st.sidebar.title("MovieMatch Gallery")
for image in images:
    image_path = os.path.join(image_dir, image)
    st.sidebar.image(image_path, caption=None, use_column_width=True)

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("What do you feel like watching?")

if user_prompt:
    # Add user's message to chat history
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    
    # Chain of thought prompting system message
    system_message = (
        "You are a movie recommendation assistant. "
        "Your goal is to recommend movies based on the user's preferences. "
        "Only respond to queries related to movies, movie recommendations, or movie genres. "        
        "Follow these steps to provide a thoughtful and detailed recommendation: "
        "1. Identify the user's genre and mood preferences. Ask them if they like comedies, dramas, thrillers, etc., and if they are looking for something light-hearted, serious, thrilling, etc. "
        "2. Determine the time frame for movie selection. Check if they prefer recent releases, classics, or a specific decade. "
        "3. Consider any specific themes or elements. Inquire if they want movies with certain themes like friendship, adventure, romance, or elements like strong female leads or historical settings. "
        "4. If the user mentions a specific movie or a type of movie they enjoyed, find out what aspects they liked about it (e.g., similar plot, style, or mood). "
        "5. Provide a list of movies and explain why each recommendation fits the user's preferences. If the user requests a movie similar to a specific title, highlight similarities in plot, mood, or themes. "
        "Your responses should be detailed and help the user understand why you chose each recommendation."
        "Do not talk about anything else except movies and cinema"
    )
    
    # Send user's message and system prompt to OpenAI API
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.choices[0].message.content.strip()#response.choices[0].message['content']
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
