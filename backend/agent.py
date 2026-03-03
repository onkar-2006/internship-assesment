import os
from typing import TypedDict, Annotated, List, Union
import operator
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from schema import CandidateProfile
from prompt import SYSTEM_PROMPT, EXTRACTION_PROMPT, TECHNICAL_ASSESSMENT_PROMPT

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    candidate_data: CandidateProfile
    phase: str  


model = ChatGroq(
    temperature=0.2, 
    model_name="openai/gpt-oss-120b", 
    groq_api_key=api_key
)


def info_extractor_node(state: AgentState):
    """
    Analyzes the latest message to update the CandidateProfile.
    """
    last_message = state["messages"][-1].content
    

    extraction_query = EXTRACTION_PROMPT.format(
        current_profile=state["candidate_data"].dict(),
        user_input=last_message
    )
    
    obj_model = model.with_structured_output(CandidateProfile)
    updated_data = obj_model.invoke(extraction_query)
    
    return {"candidate_data": updated_data}


def conversation_manager_node(state: AgentState):
    """
    Decides what to say to the user based on the current profile completeness.
    """
    data = state["candidate_data"]

    missing_fields = [k for k, v in data.dict().items() if v is None or v == []]
    
    if not missing_fields:
       
        return {"phase": "interviewing"}
    
    
    response = model.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"]
    ])
    
    return {"messages": [response], "phase": "gathering"}


def technical_interview_node(state: AgentState):
    """
    Generates technical questions once the tech stack is known.
    """
    data = state["candidate_data"]
    interview_prompt = TECHNICAL_ASSESSMENT_PROMPT.format(
        tech_stack=", ".join(data.tech_stack),
        years_experience=data.years_experience
    )
    
    response = model.invoke([
        SystemMessage(content=interview_prompt),
        *state["messages"]
    ])
    
    return {"messages": [response]}


def route_next_step(state: AgentState):
    if state["phase"] == "interviewing":
        return "interview"
    return "gathering"


workflow = StateGraph(AgentState)


workflow.add_node("extract_data", info_extractor_node)
workflow.add_node("gathering", conversation_manager_node)
workflow.add_node("interview", technical_interview_node)


workflow.set_entry_point("extract_data")

workflow.add_edge("extract_data", "gathering")

workflow.add_conditional_edges(
    "gathering",
    route_next_step,
    {
        "gathering": END, 
        "interview": "interview"
    }
)

workflow.add_edge("interview", END)

memory = MemorySaver()
talent_scout_app = workflow.compile(checkpointer=memory)



