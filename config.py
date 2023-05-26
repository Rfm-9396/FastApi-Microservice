from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_VAR = "mongodb+srv://admin:ctt123@cluster0.voemkxz.mongodb.net"  # default value if env variable does not exist
    TTL = 3600  # default value if env variable does not exist
    ENCRYPTION_KEY="Z_AhmdZgW0iLxvq-fn7ptWDyK5i5pWKrAqOymypnyjA="


settings = Settings()
