from dotenv import load_dotenv

# load .env file explicitely so that it works in production
# in dev environment the flask dev server loads it automatically

from mtg_dashboard import app as application

