import os
from pathlib import Path

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

#In future will have an AI agent to generate the project stages
PROJECT_STAGES = [
    "onboarding and environment setup",
    "learning about the SFTP requirements",
    "designing initial Spring Boot service structure",
    "exploring Snowflake DB features",
    "exploring SFTP client libraries for Java",
    "exploring the sftp file structure and data format",
    "connecting with the project manager for clarifications",
    "implementing SFTP client connection",
    "adding error handling for SFTP transfers",
    "implementing logging mechanism",
    "handling large file transfers",
    "implementing secure file transfers",
    "exploring Postgres DB features",
    "learning about postgres DB schema design",
    "learning about integrating postgres with Spring Boot",
    "implementing a data logging mechanism to log the files ingested and relevant meta data in a postgres DB",
    "exploring JSON parsing libraries for Java",
    "designing Snowflake DB schema",
    "implementing data transformation logic",
    "setting up integration tests",
    "preparing for code review",
    "addressing code review feedback",
    "preparing for deployment"
]

TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET", "")

LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_MODEL = "tbd" #might push this to an environment variable 

# Storage Settings
BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_FILE = BASE_DIR / "data" / "memories.json"

# Ensure data directory exists
(BASE_DIR / "data").mkdir(exist_ok=True)