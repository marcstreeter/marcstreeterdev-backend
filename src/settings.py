from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os
import re

URL_REGEX = re.compile(r'^https?://')

class Settings(BaseSettings):
    # Application environment
    app_env: str = Field(default="development", description="Application environment (development, production, etc.)")
    
    # CORS configuration
    cors_allow_urls: str = Field(default="")
    
    # API Keys
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    anthropic_api_key: str = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    google_api_key: str = Field(default_factory=lambda: os.getenv("GOOGLE_API_KEY", ""))
    deepseek_api_key: str = Field(default_factory=lambda: os.getenv("DEEPSEEK_API_KEY", ""))
    groq_api_key: str = Field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))

    # API URLs
    openai_api_url: str = "https://api.openai.com/v1/chat/completions"
    anthropic_api_url: str = "https://api.anthropic.com/v1/messages"
    google_api_url: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    deepseek_api_url: str = "https://api.deepseek.com/v1/chat/completions"

    # Default model names
    openai_model: str = "gpt-3.5-turbo"
    anthropic_model: str = "claude-3-opus-20240229"
    deepseek_model: str = "deepseek-chat"

    # Other constants
    llm_timeout: int = 30
    
    # Debugpy settings
    debugpy_enabled: bool = Field(default=False, description="Enable debugpy for remote debugging")
    debugpy_port: int = Field(default=5678, description="Port for debugpy to listen on")
    debugpy_wait: bool = Field(default=False, description="Whether debugpy should wait for a connection")

    @property
    def cors_allow_urls_list(self) -> List[str]:
        v = self.cors_allow_urls
        if not isinstance(v, str) or not v.strip():
            raise ValueError("CORS_ALLOW_URLS must be a non-empty comma-separated string of URLs.")
        urls = [url.strip() for url in v.split(',') if url.strip()]
        if not urls:
            raise ValueError("CORS_ALLOW_URLS must contain at least one valid URL.")
        
        valid_urls = []
        for url in urls:
            if URL_REGEX.match(url):
                valid_urls.append(url)
            else:
                raise ValueError(f"Invalid CORS origin: {url}. Must be a valid http(s) URL.")
        if not valid_urls:
            raise ValueError("CORS_ALLOW_URLS must contain at least one valid URL.")
        return valid_urls

    @property
    def is_development(self) -> bool:
        """Check if the application is running in development mode"""
        return self.app_env.lower() in ['development', 'dev']
    
    @property
    def is_production(self) -> bool:
        """Check if the application is running in production mode"""
        return self.app_env.lower() in ['production', 'prod']

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() 