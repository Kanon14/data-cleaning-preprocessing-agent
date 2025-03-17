import openai
import pandas as pd
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

# Load API key from environment file
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found in environment variables. Please set OPENAI_API_KEY in environment")

# Define the AI model
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY, temperature=0)

class CleaningState(BaseModel):
    """State schema defining input and output for the LangGraph agent."""
    input_text: str
    structured_response: str = ""

class AIAgent:
    def __init__(self):
        self.graph = self.create_graph()

    def create_graph(self):
        """Create and return a LangGraph agent graph with state management."""
        graph = StateGraph(CleaningState)

        def agent_logic(state: CleaningState) -> dict:
            """Processes the input_text using OpenAI and returns structured output."""
            try:
                response = llm.invoke(state.input_text)
                
                # Extract response correctly
                if isinstance(response, str):
                    structured_response = response
                elif hasattr(response, "content"):  # Handles AIMessage response
                    structured_response = response.content
                elif isinstance(response, dict) and "text" in response:
                    structured_response = response["text"]
                else:
                    structured_response = "No structured response received."
            
            except Exception as e:
                structured_response = f"Error processing request: {str(e)}"

            return {"input_text": state.input_text, "structured_response": structured_response}  # Ensure valid output

        graph.add_node("cleaning_agent", agent_logic)
        graph.add_edge("cleaning_agent", END)
        graph.set_entry_point("cleaning_agent")
        return graph.compile()

    def process_data(self, df, batch_size=20):
        """Processes data in batches to avoid OpenAI's token limit."""
        cleaned_responses = []

        for i in range(0, len(df), batch_size):
            df_batch = df.iloc[i:i+batch_size]  # Process in small batches
            
            prompt = f"""
            You are an AI Data Cleaning Agent. Analyze the dataset:

            {df_batch.to_string()}

            Identify missing values, choose the best imputation strategy (mean, mode, median),
            remove duplicates, and format text correctly.

            Return the cleaned data as structured text.
            """

            state = CleaningState(input_text=prompt)
            response = self.graph.invoke(state)

            # Ensure response is in the correct format
            if isinstance(response, dict):
                response = CleaningState(**response)

            cleaned_responses.append(response.structured_response)  # Store the results

        return "\n".join(cleaned_responses)  # Combine all cleaned results
