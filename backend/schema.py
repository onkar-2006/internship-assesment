from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict

class CandidateProfile(BaseModel):
    full_name: Optional[str] = Field(None, description="The candidate's full name. ")
    email: Optional[str] = Field(None, description="The candidate's email address ")
    phone: Optional[str] = Field(None, description="The candidate's contact phone number.")
    years_experience: Optional[float] = Field(None, description="Total years of professional experience.")
    desired_position: Optional[str] = Field(None, description="The job role the candidate is interested in.")
    current_location: Optional[str] = Field(None, description="The city or region where the candidate lives.")
    tech_stack: List[str] = Field(
        default_factory=list, 
        description="A list of programming languages, frameworks, and tools (e.g., ['Python', 'React', 'FastAPI']). "
    )

class ChatRequest(BaseModel):
    message: str = Field(..., example="Hi, I'm Onkar and I know Python.")
    thread_id: str = Field(..., example="unique_session_id_123")


class ChatResponse(BaseModel):
    response: str
    phase: str  
    extracted_data: Dict  



