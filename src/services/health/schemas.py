from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ProviderStatus(str, Enum):
    OK = "ok"
    FAILED = "failed"
    TIMEOUT = "timeout"
    NO_CONFIG = "no request was made because there was no configuration present for this provider"

class ProviderResult(BaseModel):
    provider: str = Field(..., description="Name of the LLM provider")
    elapsed: Optional[float] = Field(None, description="Response time in seconds")
    output: str = Field(..., description="Stringified response from the provider")
    prompt: str = Field(..., description="The prompt that was sent to the provider")
    status: ProviderStatus = Field(..., description="Status of the provider request")

class MultiTestResponse(BaseModel):
    results: List[ProviderResult] = Field(..., description="Results from all tested providers")

class LLMRequest(BaseModel):
    prompt: Optional[str] = Field(
        default="give me the name of the main villain's cat in the show the smurfs",
        description="The prompt to send to all LLM providers"
    )
