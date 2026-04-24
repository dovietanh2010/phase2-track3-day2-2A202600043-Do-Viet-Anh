import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Model configuration
MODEL_NAME = "gpt-5.4-mini"

# Memory paths
USER_PROFILE_PATH = "data/user_profile.json"
EPISODES_PATH = "data/episodes.json"
CHROMA_DB_DIR = "data/chroma_db"
