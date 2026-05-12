import os
from pathlib import Path
from dotenv import load_dotenv

base_dir = Path(__file__).parent
env_dir = base_dir / ".env"

load_dotenv(env_dir)


class Config:
    REPO_NAME = os.getenv("REPO_NAME")
    REPO_OWNER = os.getenv("REPO_OWNER")
