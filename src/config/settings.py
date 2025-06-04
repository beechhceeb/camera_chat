from pathlib import Path


ROOT = Path(__file__).parent.parent.parent

GOOGLE_CLOUD_PROJECT = "mpb-data-science-dev-ab-602d"
GOOGLE_CLOUD_DATASET = "dsci_pricing_model"
GOOGLE_CLOUD_LOCATION = "us-central1"
GOOGLE_GENAI_USE_VERTEXAI = True
MODEL = "gemini-2.0-flash-001"

QUERY = "get_raw_model_database"
DB_PROMPT_SAVE_PATH = ROOT / "data" / "db_prompt.txt"
