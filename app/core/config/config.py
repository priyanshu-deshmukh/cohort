from pydantic_settings import BaseSettings
import uuid

class Settings(BaseSettings):

    DB_USERNAME: str
    DB_NAME: str
    DB_PORT: int
    DB_HOST: str
    DB_PASSWORD: str


    SUPERADMIN_ID: uuid.UUID
    SUPERADMIN_EMAIL: str
    SUPERADMIN_PASSWORD: str
    SUPERADMIN_NAME: str


    ROLES: list[str]
    ROLE_IDS: list[uuid.UUID]

    SECRET_KEY: str
    ALGORITHM: str


    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_PRESIGNED_URL_EXP: int
    REGION: str
    BUCKET_NAME: str

    TEMP_LOCAL_PATH: str

    SES_SENDER_MAIL: str

    @property
    def DB_URL(self):
        return f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    model_config = {
        'env_file': ".env"
    }

settings = Settings()