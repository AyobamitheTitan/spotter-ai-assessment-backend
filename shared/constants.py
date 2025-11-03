import os

from dotenv import load_dotenv

load_dotenv()
CONSTANTS = {"BASE_OPEN_ROUTE_URL": os.getenv("BASE_OPEN_ROUTE_URL")}
