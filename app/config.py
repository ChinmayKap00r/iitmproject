import os
from dotenv import load_dotenv

load_dotenv()

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
