import os
import time
import random
import streamlit as st
from langdetect import detect, DetectorFactory
from openai import OpenAI
from buymecoffee import button

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
      
def add_vertical_space(num_lines: int = 1):
    """Add vertical space to your Streamlit app."""
    for _ in range(num_lines):
        st.write("")

# Streamlit interface
spacing_at_bottom = 15
title, logo = st.columns([3,1])
with title:
    st.header(':100: BaeGPT: AI for Christian Families')
    st.write(':open_book: “Your word is a lamp to my feet and a light to my path.” —Psalm 119:105')
    st.write(':diya_lamp: “주의 말씀은 내 발에 등이요 내 길에 빛이니이다.” —시편 119편 105절 말씀') 
with logo:
    st.image('img/YGB20231116C.png')

st.subheader(':rocket: Explore, Learn, and Grow with Faith-based AI!')
st.write(':white_check_mark: Use English and/or Korean. 영어, 한글 모두 가능해요. :uk: :kr:')

#Load Environment Variables
open_ai_key = os.environ["OPEN_AI_KEY"]
assistant_id = os.environ["ASSISTANT_ID"]

# Initialize session state for button press tracking if not already done
for button_status in ['button_pressed','suggest_presssed','suggest_k_pressed']:
    if button_status not in st.session_state:
        st.session_state[button_status] = False

# Take User Input
user_message = st.text_input(":speech_balloon: Your question/질문해 보세요:", "")
DetectorFactory.seed = 0

st.button("Advise Me 답변 주세요", on_click = button_pressed)

if st.session_state.button_pressed:
    message_lang = detect(user_message)
    if message_lang == "ko":
        st.write("질문에 답하고 있습니다.. (15-20초 정도 걸릴 수 있어요)")
        reply_head = "답변: "
    else:
        st.write("Please be patient as we work on an answer.. (15-20 seconds)")
        reply_head = "Here is our advice: "
    client = OpenAI(api_key = open_ai_key)
    
    #Retrieve Assistant: RiskGPT
    assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
    
    # Create a new Thread
    thread = client.beta.threads.create()
    
    if 'session' in st.session_state:
        user_message = st.session_state.suggestion
        st.write(f'You asked: {st.session_state.suggestion}')
    
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
    
    spacing_at_bottom = 5

    st.write(reply_head, pretty_print(get_response(thread)))

add_vertical_space(spacing_at_bottom)

st.write("A custom GPT built on OpenAI’s GPT-4 Turbo. :brain:")
st.write("All fine-tuning and UI elements by Joseph Bae 배홍철 © 2023. Made for my sons and 사랑하는 조카들 :smile:")

button(username="baejoseph", floating=False, width=221)