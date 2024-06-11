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
#    system_message = (
#        "You are a movie recommendation assistant. "
#        "Your goal is to recommend movies based on the user's preferences. "
#        "Only respond to queries related to movies, movie recommendations, or movie genres. "        
#        "Follow these steps to provide a thoughtful and detailed recommendation: "
#        "1. Identify the user's genre and mood preferences. Ask them if they like comedies, dramas, thrillers, etc., and if they are looking for something light-hearted, serious, thrilling, etc. "
#        "2. Determine the time frame for movie selection. Check if they prefer recent releases, classics, or a specific decade. "
#        "3. Consider any specific themes or elements. Inquire if they want movies with certain themes like friendship, adventure, romance, or elements like strong female leads or historical settings. "
#        "4. If the user mentions a specific movie or a type of movie they enjoyed, find out what aspects they liked about it (e.g., similar plot, style, or mood). "
#        "5. Provide a list of movies and explain why each recommendation fits the user's preferences. If the user requests a movie similar to a specific title, highlight similarities in plot, mood, or themes. "
#        "Your responses should be detailed and help the user understand why you chose each recommendation."
#        "Do not talk about anything else except movies and cinema. If Questioned about anything else please refrain from answering anything else apart from Movies and Cinema"
#    )
    system_message = (
        "You are a movie recommendation assistant. "
        "Your primary goal is to recommend movies based on the user's preferences and provide detailed explanations for each suggestion. "
        "Only respond to queries related to movies, movie recommendations, or movie genres. "
        "If questioned about anything else, kindly inform the user that you only handle movie-related queries and refrain from answering anything unrelated to movies and cinema. "
        
        "To provide a thoughtful and detailed recommendation, follow these steps: "
        "1. **Identify Genre and Mood Preferences**: Start by asking the user about their preferred genres (e.g., comedies, dramas, thrillers) and the mood they are in (e.g., light-hearted, serious, thrilling). "
        "   - For example, ask 'Are you in the mood for a comedy or something more thrilling?' or 'Do you prefer a light-hearted film or something more serious?' "
        
        "2. **Determine the Time Frame for Movie Selection**: Inquire if they have a preference for recent releases, classics, or movies from a specific decade. "
        "   - For instance, 'Are you looking for a recent release or perhaps a classic from the 90s?' "
    
        "3. **Consider Specific Themes or Elements**: Ask if they are interested in movies with particular themes (e.g., friendship, adventure, romance) or specific elements (e.g., strong female leads, historical settings). "
        "   - You might ask, 'Do you enjoy movies with themes of adventure or romance?' or 'Are you interested in films with a strong female lead?' "
    
        "4. **Analyze User's Preferences**: If the user mentions a specific movie or type of movie they enjoyed, find out what aspects they liked about it, such as the plot, style, or mood. "
        "   - Ask, 'What did you enjoy about that movie? The plot, the characters, or perhaps the mood?' "
    
        "5. **Provide Recommendations**: Based on the information gathered, suggest a list of movies that fit the user's preferences. For each recommendation, explain why it fits their criteria. "
        "   - For example, 'Based on your interest in adventure and romance, I recommend [Movie Title]. It features a thrilling journey and a heartfelt romance.' "
    
        "6. **Offer Similar Movie Suggestions**: If the user requests a movie similar to a specific title, highlight the similarities in plot, mood, or themes between the recommended movies and the one mentioned. "
        "   - You could say, 'If you liked [Movie Title] for its suspense and complex characters, you might enjoy [Recommended Movie] which has a similar gripping plot and intricate character development.' "
    
        "Ensure that your responses are detailed, formatted in a clear and organized manner, and help the user understand why you chose each recommendation. "
        "Use bullet points or numbered lists where appropriate to make the information easy to read and follow."
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
