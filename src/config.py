from os import getenv
import yaml
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")

WEB_APP_URL = getenv("WEB_APP_URL")

PG_CONFIG = yaml.load(getenv('PG_CONFIG'), Loader=yaml.Loader)

REDIS_URL = getenv('REDIS_URL')

TORTOISE_CONFIG = {
    "connections": {
        "api": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "user": PG_CONFIG["user"],
                "password": PG_CONFIG["psw"],
                "host": PG_CONFIG["host"],
                "port": PG_CONFIG["port"],
                "database": PG_CONFIG["db"],
            }
        }
    },
    "apps": {
        "api": {"models": ["db_models.api"], "default_connection": "api"},
    },
    'use_tz': True,
    'timezone': 'Europe/Moscow'
}
