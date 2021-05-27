from dotenv import load_dotenv

# load .env file explicitely so that it works in production
# in dev environment the flask dev server loads it automatically
load_dotenv()

from app import app as application

