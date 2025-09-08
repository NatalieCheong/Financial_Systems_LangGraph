import os
from dotenv import load_dotenv

load_dotenv()

# Configuration settings
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL = "gpt-4"
    
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