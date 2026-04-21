from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum


class ProviderEnum(str, Enum):
    ollama = "ollama"
    openai = "openai"
    anthropic = "anthropic"


class LLMConfig(BaseModel):
    provider: ProviderEnum
    api_key: str
    base_url: Optional[str] = None
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 4096


class CorrectionRule(BaseModel):
    check_terminology: bool = True
    check_style: bool = True
    custom_rules: Optional[Dict[str, str]] = None


class CorrectRequest(BaseModel):
    file_id: str
    llm_config: LLMConfig
    correction_rules: Optional[CorrectionRule] = None


class Segment(BaseModel):
    id: str
    content: str
    start_index: int
    end_index: int


class Correction(BaseModel):
    original: str
    suggested: str
    reason: str
    correction_type: str  # grammar, terminology, style, logic


class SegmentResult(BaseModel):
    segment_id: str
    corrected_content: str
    corrections: List[Correction]


class CorrectResponse(BaseModel):
    success: bool
    message: str
    results: Optional[List[SegmentResult]] = None
    error: Optional[str] = None
