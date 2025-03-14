import openai
import pandas as pd
from dotenv import load_dotenv
import os
from langchain_openai import OpenAI
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

# Load API key from environment file
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found in environment variables. Please set OpenAI_API_KEY in environment")

# Define the AI model
llm = OpenAI(model="gpt-4o", api_key=OPENAI_API_KEY, temperature=0)

class CleaningState(BaseModel):
    """State schema defining input and output for the LangGraph agent."""
    input_text: str
    structured_response: str = ""
    
class AIAgent:
    def __init__(self):
        self.graph = self.create_graph()
        
    def create_graph(self):
        """Create and returns a LangGraph agent graph with state management."""
        graph = StateGraph(CleaningState)
        
        # FIX: Ensure agent outputs structured response
        def agent_logic(state: CleaningState) -> CleaningState:
            response = llm.invoke(state.input_text)
            return CleaningState(input_text=state.input_text, structured_response=response) # Ensuring strucutured response
        
        graph.add_node("cleaning_agent", agent_logic)
        graph.add_edge("cleaning_agent", END)
        graph.set_entry_point("cleaning_agent")
        return graph.compile()
    
    def process_data(self, df, batch_size=20):
        """Processes data in batches to avoid OpenAI's token limit."""
        cleaned_response = []
        
        for i in range(0, len(df), batch_size):
            df_batch = df.iloc[i:i+batch_size] # Process 20 rows at a time
            
            prompt = f"""
            You are an AI Data Cleaning Agent. Analyze the dataset:
            
            {df_batch.to_string()}
            
            Identify missing values, choose the best imputation strategy (mean, mode, median),
            remove duplicats, and format text correctly.
            
            Return the cleaned data as structured text.
            """
            
            state = CleaningState(input_text=prompt, structured_response="")
            response = self.graph.invoke(state)
            
            if isinstance(response, dict):
                response = CleaningState(**response)
                
            cleaned_response.append(response.structured_response) # Store the results
            
        return "\n".join(cleaned_response) # Combine all cleaned results