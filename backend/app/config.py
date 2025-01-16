from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_hostname : str
    database_password : str
    database_username : str
    database_name : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    #class Config: ----deprecated
    #    env_file = ".env"
    
    model_config = SettingsConfigDict(
        env_file=".env",  # Path to your .env file
        env_file_encoding="utf-8", # Important for different character encodings
        case_sensitive=False, #environment variables are case insensitive by default
        #env_prefix="MY_APP_" #add a prefix to the env variables to avoid conflicts
    )

Settings = Settings()