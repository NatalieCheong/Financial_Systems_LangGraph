import os
from dotenv import load_dotenv

load_dotenv()

# Configuration settings
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL = "gpt-4"

    # LangSmith configuration
    if os.getenv("LANGCHAIN_TRACING_V2"):
        os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
        os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT")
        os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
        os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "financial-analysis")
        
    # Financial analysis parameters
    DEFAULT_PERIOD = "1y"  # 1 year
    DEFAULT_INTERVAL = "1d"  # daily
    
    # Report settings
    REPORT_OUTPUT_DIR = "reports"
    CHART_OUTPUT_DIR = "charts"
    
    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Create output directories if they don't exist
        os.makedirs(cls.REPORT_OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.CHART_OUTPUT_DIR, exist_ok=True)
