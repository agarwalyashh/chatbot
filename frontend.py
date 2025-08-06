import streamlit as st
from backend import workflow,model
from langchain_core.messages import HumanMessage
import uuid

def generate_uniqueId():
    return (uuid.uuid4())

def reset_chat():
    st.session_state['message_history'] = []
    thread_id = generate_uniqueId()
    st.session_state['thread_id'] = thread_id
    st.session_state['chat_thread'].append({'title':'New Chat','thread_id':thread_id})
    st.session_state['start'] = True
    
def load_conversation(thread_id):
    state = workflow.get_state(config={'configurable':{'thread_id':thread_id}}).values
    if state:
        return state['messages']
    return []
    
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = [] # Normal list can't be used as whenever we enter an input text, entire file executes and [] is initialized again
if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread'] = []
if 'thread_id' not in st.session_state:
    thread_id = generate_uniqueId()
    st.session_state['thread_id'] = thread_id
    st.session_state['chat_thread'].append({'title':'New Chat','thread_id':thread_id})
if 'start' not in st.session_state:
    st.session_state['start'] = True
    
st.sidebar.title('Langgraph Chatbot')
if st.sidebar.button('Start a New Chat'):
    reset_chat()
st.sidebar.header('Previous Conversations')

for chat in st.session_state['chat_thread'][::-1]:
    if st.sidebar.button(str(chat['title']),key=str(chat['thread_id'])):
        st.session_state['thread_id'] = chat['thread_id']
        messages = load_conversation(chat['thread_id'])
        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                temp_messages.append({'role': 'user', 'content': message.content})
            else:
                temp_messages.append({'role': 'assistant', 'content': message.content})
        st.session_state['message_history'] = temp_messages
        
for i in st.session_state['message_history']:
    with st.chat_message(i['role']):
        st.text(i['content'])

user_input = st.chat_input('Type Here...')

if user_input and st.session_state['start']:
    prompt = f'Generate a 2-3 word headline for a conversation {user_input} for my chatbot flow. Nothing else is needed'
    result = model.invoke(prompt).content
    st.session_state['chat_thread'][-1]['title'] = result
    st.session_state['start'] = False

if(user_input):
    st.session_state['message_history'] .append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk,metadata in workflow.stream(
                {'messages':[HumanMessage(content = user_input)]},config = {'configurable':{'thread_id':st.session_state['thread_id']}},stream_mode = 'messages')
        )
        st.session_state['message_history'].append({'role':'assistant','content':ai_message})