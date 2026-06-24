from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DB_USERNAME: str
    DB_NAME: str
    DB_PORT: int
    DB_HOST: str
    DB_PASSWORD: str


    SUPERADMIN_EMAIL: str
    SUPERADMIN_PASSWORD: str
    SUPERADMIN_NAME: str


    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    model_config = {
        'env_file': ".env"
    }

settings = Settings()