#Author: Bogdan Nalyvaiko
#This code provides an example of a simple page built in Streamlit to integrate HugginFace's LLMs.
#Required libraries: streamlit, hugchat
#Run the code in the terminal, using the following command
# streamlit run {.py_file_location}/simple_streamlit_interface_for_AI_chatbot.py
#My example:      streamlit run c:/Users/bbnfa/Python_bgdn/AI_chatbot/simple_streamlit_interface_for_AI_chatbot.py

from datetime import datetime as dt
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.set_page_config(layout="wide", page_title="🤗💬 HugChat")
st.title("Simple chatbot: HugChat")

# Log in to huggingface and grant authorization to huggingchat
sign = Login('your_email@email_provider.com', 'your_password') #replace with your login and password to hugface
cookies = sign.login()

# start a new huggingchat connection
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

# start a new conversation
conv_id = chatbot.new_conversation()
chatbot.change_conversation(conv_id)
    
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    start_message = str(fr"[{dt.now().strftime('%d/%m/%Y %H:%M:%S')}]: How may I help you?")
    st.session_state.messages = [{"role": "assistant", "content": start_message}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input):
    return chatbot.chat(prompt_input)

# User-provided prompt
if prompt := st.chat_input():
    prompt_with_time_stamp = str(fr"[{dt.now().strftime('%d/%m/%Y %H:%M:%S')}]: {prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt_with_time_stamp})
    with st.chat_message("user"):    
        st.write(prompt_with_time_stamp)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt) 
            response_with_time_stamp = str(fr"[{dt.now().strftime('%d/%m/%Y %H:%M:%S')}]: {response}")
            st.write(response_with_time_stamp) 
    message = {"role": "assistant", "content": response_with_time_stamp}
    st.session_state.messages.append(message)
