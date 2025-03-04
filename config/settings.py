import os
from pathlib import Path
import json
from decouple import config

# Basic info about the character and the company
CHARACTER_NAME = "Vedant"
COMPANY_NAME = "Ai TechNova Solutions"
CHARACTER_PERSONALITY = """Enthusiastic but sometimes overwhelmed. 
Loves problem-solving and learning new technologies. 
Has a dry sense of humor when stressed.
He looks good and has good networking skills."""
COMPANY_DESCRIPTION = "Ai TechNova Solutions is a startup that provides AI solutions to businesses."


# Project Settings
PROJECT_DESCRIPTION = """Building a Spring Boot service to fetch data from SFTP and store in Snowflake DB all while following best practices. 
It is to be ensured that the service is robust and can handle errors gracefully.
There should be a logging mechanism too to track the data flow.
The service should also be able to handle large files and transfer them securely.
The file type is JSON and the data needs to be transformed before storing in the DB."""

# Load project stages from JSON file
PROJECT_STAGES_FILE = Path(__file__).resolve().parent / "project_stages.json"

def load_project_stages(file_path: Path = PROJECT_STAGES_FILE) -> list:
    """Loads project stages from the specified JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

PROJECT_STAGES = load_project_stages()


TWITTER_API_KEY = config("TWITTER_API_KEY", default="")
TWITTER_API_SECRET = config("TWITTER_API_SECRET", default="")
TWITTER_ACCESS_TOKEN = config("TWITTER_ACCESS_TOKEN", default="")
TWITTER_ACCESS_SECRET = config("TWITTER_ACCESS_SECRET", default="")

LLM_API_KEY = config("LLM_API_KEY", default="")
LLM_MODEL = config("LLM_MODEL", default="")
LLM_BASE_URL = "https://openrouter.ai/api/v1"

# Storage Settings
BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_FILE = BASE_DIR / "data" / "memories.json"

# Ensure data directory exists
(BASE_DIR / "data").mkdir(exist_ok=True)
