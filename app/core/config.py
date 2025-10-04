from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str

    NASA_TOKEN: str
    OWM_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
