import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pentzy:pentzy@db:5432/pentzydb"
)
