# Data Cleaning Agent

## Overview
A robust pipeline to handle the messy data from various sources via AI-powered agent. It supports data ingestion from CSV/Excel files, Databased queries, and API endpoints. 

## Project Setup
### Prerequisites
- Python 3.8+
- PyTorch 1.8+
- Compatible cuda toolkit and cudnn installed on your machine.
- Anaconda or Miniconda installed on your machine.

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Kanon14/data-cleaning-preprocessing-agent.git
cd data-cleaning-preprocessing-agent
```

2. Create and activate a Conda environment:
```bash
conda create -n dc-agent python=3.8 -y
conda activate dc-agent
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Workflow:
1. **Data Ingestion:** Users can upload either CSV/Excel; SQL Queries from DB, or API Endpoints. 
2. **Data Cleaning:** 
- Rule-Based Cleaning:
    * Handles missing values
    * Removes duplicates
    * Standardizes column formats
- AI-Powered Agent:
    * Uses LangChain Agent to enhance data quality
    * Automates complex transformations
3. **Processing & Execution:** 
- Frontend: Streamlit application that accepts user input and send requests to FastAPI for processing.
- Backend: Handles requests and processes data.
