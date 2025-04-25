import os

# Default values if environment variables are not set
DEFAULT_LOOKBACK_DURATION = "30d"
DEFAULT_CHUNK_SIZE = 5
DEFAULT_DEBUG = False
#NAMESPACES = ["threescale"]
#PROMETHEUS_URL = "http://prometheus.threescale.apps.mstoklus.giq5.s1.devshift.org/"

NAMESPACES = os.environ.get("NAMESPACES", "<TARGET_NAMESPACE/S").split(',')
PROMETHEUS_URL = os.environ.get("PROMETHEUS_URL", "<PROMETHEUS ROUTE>")
LOOKBACK_DURATION = os.environ.get("LOOKBACK_DURATION", DEFAULT_LOOKBACK_DURATION)
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", DEFAULT_CHUNK_SIZE))
DEBUG = os.environ.get("DEBUG", str(DEFAULT_DEBUG)).lower() == 'true'

# # Optional: Print the loaded configuration to verify
# if DEBUG:
#     print("Loaded Configuration:")
#     print(f"NAMESPACES: {NAMESPACES}")
#     print(f"PROMETHEUS_URL: {PROMETHEUS_URL}")
#     print(f"LOOKBACK_DURATION: {LOOKBACK_DURATION}")
#     print(f"CHUNK_SIZE: {CHUNK_SIZE}")
#     print(f"DEBUG: {DEBUG}")

