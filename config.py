import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    #gemini apikey configration
     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

     GEMINI_MODEL="gemini-2.5-flash-lite"


     #agent configration

     MAX_ITTRATION=3

     TEMPERATURE= 0.1

     #search configration

     SEARCH_REASULTS_LIMITS = 2

     #UI configration 

     STREAMLIT_TITLE="ReAct Agent - Reasoning and Acting"

     STREAMLIT_DISCRIPTION = """
    This ReAct Agent demostrate the Reasoning and Acting loop
    1. **Reasoning**: the agent think throw problem step by step
    2. **Acting**: the agent takes action to gather information
    3. **Loop**: the process repeats untill the action is complete
    """
     def validate_config(clas):
          if not clas.GEMINI_API_KEY:
               raise ValueError(
                    "GEMINI_API_KEY npot found in environment variable"
                    "please set it in your .env file or environment"
               )
          return True 
          
