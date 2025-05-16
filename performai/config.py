import os

# Default values if environment variables are not set
DEFAULT_LOOKBACK_DURATION = "30d"
DEFAULT_CHUNK_SIZE = 5
DEFAULT_DEBUG = False
DEFAULT_LLM_MODEL = "mistral"
DEFAULT_USE_LOCAL_LLM = True
DEFAULT_PROMETHEUS_URL = "http://prometheus.threescale.apps.mstoklus.giq5.s1.devshift.org/" # set default

# Load from environment variables, overriding defaults if set
NAMESPACES = os.getenv("NAMESPACES", "threescale").split(',')
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", DEFAULT_PROMETHEUS_URL)
LOOKBACK_DURATION = os.getenv("LOOKBACK_DURATION", DEFAULT_LOOKBACK_DURATION)
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", str(DEFAULT_CHUNK_SIZE)))
DEBUG = os.getenv("DEBUG", str(DEFAULT_DEBUG)).lower() == "true"
LLM_HOSTED_URL = os.getenv("LLM_HOSTED_URL", "")  # Default to empty string
LLM_API_TOKEN = os.getenv("LLM_API_TOKEN", "")  # Default to empty string
LLM_MODEL = os.getenv("LLM_MODEL", DEFAULT_LLM_MODEL)
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", str(DEFAULT_USE_LOCAL_LLM)).lower() == "true"


