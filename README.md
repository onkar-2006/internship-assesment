
# TalentScout | Intelligent Hiring Assistant 

TalentScout is a professional AI-driven recruitment assistant designed to automate the initial screening of technology candidates. Built with an **Agentic AI** architecture, it engages candidates in a natural conversation to extract key information and generate customized technical assessments.

## 1. Project Overview
The TalentScout assistant streamlines the top-of-the-funnel hiring process by:
* **Initial Greeting:** Welcoming candidates and providing a brief overview of the assistant's purpose.
* **Structured Data Extraction:** Automatically identifying Name, Email, Phone, Experience, Location, and Current Position from unstructured chat.
* **Tech Stack Identification:** Capturing programming languages, frameworks, and tools the candidate is proficient in.
* **Dynamic Technical Assessment:** Generating 3-5 tailored technical questions based on the declared tech stack to evaluate proficiency.
* **Context Awareness:** Maintaining conversation flow and handling follow-up questions seamlessly.

## 2. Technical Details

### Architectural Decisions
I implemented a **Microservices Architecture** to separate the user interface from the AI orchestration logic:
* **Backend (FastAPI):** Acts as the core API, handling the orchestration layer, LLM calls, and state management.
* **Frontend (Streamlit):** Provides a clean, intuitive UI for candidates with a real-time data extraction sidebar.
* **Orchestration (LangGraph):** Manages the conversation flow as a **State Machine**, ensuring the bot follows logic-based nodes.


### Libraries & Models
* **LLM:** GPT:oss-120B (via **Groq API**) for ultra-fast, sub-second inference speed.
* **Frameworks:** LangGraph, LangChain, Pydantic (for strict data validation).
* **Infrastructure:** Docker & Docker Compose for containerization and local deployment.

## 3. Prompt Design
The intelligence of the assistant is driven by two primary prompt engineering strategies:
1. **The Information Extractor:** A system prompt that instructs the LLM to act as a structured data parser, mapping natural language into a **Pydantic schema**.
2. **The Technical Interviewer:** A dynamic prompt that utilizes the extracted "Tech Stack" to generate relevant, challenging technical questions.


## 4. Project Structure
```
    
    INTERNSHIP_ASSEMENT/
    ├── backend/
    │   ├── agent.py         # LangGraph logic & State definition
    │   ├── main.py          # FastAPI entry point
    │   ├── prompt.py        # System and extraction prompts
    │   ├── schema.py        # Pydantic models for data validation
    │   ├── Dockerfile       # Backend containerization
    │   └── requirements.txt # Backend dependencies
    ├── frontend/
    │   ├── app.py           # Streamlit UI
    │   ├── Dockerfile       # Frontend containerization
    │   └── requirements.txt # Frontend dependencies
    ├── README.md            # Project documentation
    └── render.yaml          # Cloud deployment configuration

```

## 4. Installation Instructions


* A Groq Cloud API Key.

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/onkar-2006/internship-assesment.git](https://github.com/onkar-2006/internship-assesment.git)
   cd internship-assesment
    

2.  **Environment Variables.**
    ```
    Create a .env file in the  in root directory to store your credentials:
    GROQ_API_KEY=your_api_key_here


3: Run the Backend (FastAPI)
    
    Open a new terminal window:
  
    cd backend
    python -m venv venv
    source venv/bin/activate  # Windows: .venv\\Scripts\\activate
    pip install -r requirements.txt
    python main.py
    The backend will now be running at: http://localhost:8000

Step 4: Run the Frontend (Streamlit)
Open another separate terminal window:

Bash
    
    cd frontend
    python -m venv venv
    source venv/bin/activate  # Windows: .venv\\Scripts\\activate
    pip install -r requirements.txt
    streamlit run app.py
    The frontend will now be running at: http://localhost:8501



## 5. Usage Guide

### Conversational Workflow
I designed the interaction to be goal-oriented, moving the candidate through specific screening phases:
* **Start the Chat:** Initiate the session by greeting the bot (e.g., "Hi, I am Onkar") to trigger the recruitment overview.
* **Provide Details:** Follow the natural prompts to provide essential contact information, years of experience, and current location.
* **Declare Tech Stack:** Specify your core competencies (e.g., "I am proficient in Python and React") to allow the AI to prepare the assessment.
* **Technical Interview:** Engage with 3-5 technical questions generated dynamically for your specific stack to demonstrate proficiency.
* **Exit the Session:** Use a conversation-ending keyword (e.g., "Exit," "Goodbye," or "Quit") to conclude the interaction gracefully.

## 6. Challenges & Solutions

### Engineering Hurdles
During development, I addressed several technical challenges to ensure system stability and performance:
* **State Initialization:** I solved early system crashes by **"seeding" the LangGraph state** with a default Pydantic model at the start of every session to prevent empty-field errors.
* **Deployment Latency:** I optimized the frontend timeout settings and implemented **health-check pings** to mitigate 502 errors caused by Render's "cold start" behavior.
* **Data Consistency:** I utilized **Pydantic validation** to force the LLM output into a strict structure, ensuring the frontend sidebar and backend logic handle data reliably without malformed JSON errors.

