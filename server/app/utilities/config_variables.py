import os

# Database Config
MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# App Config
FASTAPI_PORT_NUMBER = int(os.getenv("FASTAPI_PORT_NUMBER", default=30000))
FASTAPI_HOST = os.getenv("FASTAPI_HOST", default="0.0.0.0")

# REDIS
REDIS_HOST = os.getenv("REDIS_HOST", default="0.0.0.0")
REDIS_PORT = int(os.getenv("REDIS_PORT", default=3))
REDIS_DATABASE = int(os.getenv("REDIS_DATABASE", default=3))
REDIS_TTL = int(os.getenv("REDIS_TTL", default=900))
REDIS_CONNECT_TIMEOUT = int(os.getenv("REDIS_CONNECT_TIMEOUT", default=10))

# AWS DynamoDB
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# Auth Config
SECRET_KEY = os.getenv("SECRET_KEY", default='SECRET_kEY')
ALGORITHM = os.getenv("ALGORITHM", default="hs12")

# ALLOWED ORIGINS
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", default="https://YTSAF.com")

MAX_PLAYERS_PER_GROUP = int(os.getenv("MAX_PLAYERS_PER_GROUP", default=5))
