from fastapi import Depends

from config import Settings

aa = Settings()
print(aa.MONGO_VAR)