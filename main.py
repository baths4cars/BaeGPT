import os
import time
import random
import streamlit as st
from openai import OpenAI

# Helpful functions
def button_pressed()->None:
    st.session_state.button_pressed = True
    suggestion = user_message

def random_line_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                return random.choice(lines).strip()
            else:
                return "The file is empty."
    except Exception as e:
        return f"Error: {str(e)}"

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id = thread.id,
            run_id = run.id,
        )
        time.sleep(1.5)
    return run

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order='asc')

def pretty_print(messages):
    for m in messages:
        if m.role == "assistant":
          return f"{m.content[0].text.value}"

# Streamlit interface
title, logo = st.columns([3,1])
with title:
    st.title(':100: BaeGPT: Ask away!')
    st.header(':rocket: 인생의 궁금한 뭐든지 물어보세요!') 
    st.write(':white_check_mark: Use English and/or Korean. 영어, 한글 모두 가능해요. :uk: :kr: ')
with logo:
    st.image('img/YGB20231116C.png')

#Authenticate
open_ai_key = os.environ["OPEN_AI_KEY"]

# Initialize session state for button press tracking if not already done
if 'button_pressed' not in st.session_state:
    st.session_state.button_pressed = False
    
    suggestion = random_line_from_file('suggested_questions.txt')
    
suggestion = 'hot cake'

# Take User Input
user_message = st.text_input(":speech_balloon: Your question/질문해 보세요:", suggestion)

st.button("Advise Me", on_click = button_pressed)

if st.session_state.button_pressed:
    client = OpenAI(api_key = open_ai_key)
    
    #Retrieve Assistant: RiskGPT
    assistant_id = 'asst_ItjOa3iOaYSOoUKCAvy0cGkc'
    assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
    
    # Create a new Thread
    thread = client.beta.threads.create()
    
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    run = wait_on_run(run,thread)

    st.write("Here is our advice: ", pretty_print(get_response(thread)))


st.write("2023 Copyright Joseph Bae 배홍철. Made for my sons and 사랑하는 조카들 :smile:")