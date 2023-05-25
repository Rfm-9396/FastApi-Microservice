from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_VAR = "mongodb+srv://admin:ctt123@cluster0.voemkxz.mongodb.net"  # default value if env variable does not exist



settings = Settings()
