import streamlit as st
from backend import workflow
from langchain_core.messages import HumanMessage

config = {'configurable':{'thread_id':1}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = [] # Normal list can't be used as whenever we enter an input text, entire file executes and [] is initialized again

for i in st.session_state['message_history']:
    with st.chat_message(i['role']):
        st.text(i['content'])

user_input = st.chat_input('Type Here...')

if(user_input):
    st.session_state['message_history'] .append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    response = workflow.invoke({'messages':[HumanMessage(content = user_input)]},config = config)
    response = response['messages'][-1].content
    st.session_state['message_history'] .append({'role':'assistant','content':response})
    with st.chat_message('assistant'):
        st.text(response)