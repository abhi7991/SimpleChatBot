# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 22:08:50 2024

@author: abhis
"""

import streamlit as st
import openai
from streamlit_chat import message
import os
from dotenv import load_dotenv
import pandas as pd
import requests

def load_env_variables():
    load_dotenv()
    openai.api_key = os.environ.get('OPENAI_API_KEY')

def api_calling(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message

def get_text():
    input_text = st.text_input("Write here:", key="input")
    return input_text

def initialize_session_state():
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = []
    if 'openai_response' not in st.session_state:
        st.session_state['openai_response'] = []

def display_chat_history():
    if st.session_state['user_input']:
        for i in range(len(st.session_state['user_input']) - 1, -1, -1):
            # Display user input
            message(st.session_state["user_input"][i], key=str(i), avatar_style="icons")
            # Display OpenAI response
            message(st.session_state['openai_response'][i], avatar_style="miniavs", is_user=True, key=str(i) + 'data_by_user')

def main():
    load_env_variables()
    
    st.title("ChatGPT ChatBot With Streamlit and OpenAI")
    
    initialize_session_state()
    
    user_input = get_text()
    
    if user_input:
        output = api_calling(user_input)
        output = output.lstrip("\n")
        # Store the output
        st.session_state.openai_response.append(user_input)
        st.session_state.user_input.append(output)
    
    display_chat_history()

if __name__ == "__main__":
    main()
