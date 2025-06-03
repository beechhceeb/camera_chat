import os
from dotenv import load_dotenv
import logging

load_dotenv()


def parse_bool(val):
    return str(val).lower() in ("1", "true", "yes", "on")


# Determine log level from environment
log_level = os.getenv("LOG_LEVEL")
if log_level is None:
    debug_env = os.getenv("DEBUG", "False")
    debug = parse_bool(debug_env)
    log_level = "DEBUG" if debug else "INFO"

# Only configure root logger if not already configured
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
