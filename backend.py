from langgraph.graph import StateGraph,START,END
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

class BotState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages] 
    
model = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash')
def chatFunction(state:BotState):
    messages = state['messages']
    result = model.invoke(messages)
    return {'messages':result}

checkpointer = InMemorySaver()
graph = StateGraph(BotState)

graph.add_node('chat',chatFunction)

graph.add_edge(START,'chat')
graph.add_edge('chat',END)

workflow = graph.compile(checkpointer = checkpointer)