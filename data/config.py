"""
This is configuration file
You should rename env-example.env to .env and put in it your data
"""

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Taking Bot token
ADMINS = env.list("ADMINS")  # Taking Bot token

DB_USER = env.str("DB_USER")  # Taking database username
DB_PASS = env.str("DB_PASS")  # Taking database password
DB_NAME = env.str("DB_NAME")  # Taking database name
DB_HOST = env.str("DB_HOST")  # Taking database host
DB_PORT = env.int("DB_PORT")  # Taking database port
I18N_DOMAIN = ''  #
LOCALES_DIR = ''  #
