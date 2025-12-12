import os
from dotenv import load_dotenv
load_dotenv()
from config import OPENAI_API_KEY

if not OPENAI_API_KEY:
    raise EnvironmentError("Set OPENAI_API_KEY in environment or .env file before running.")

from runner import main
if __name__ == "__main__":
    main()
