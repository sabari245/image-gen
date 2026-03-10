from datetime import datetime

from pydantic import BaseModel, Field


class GenerationConfig(BaseModel):
    aspect_ratio: str = "1:1"
    resolution: str = "2K"
    thinking_level: str = "high"
    temperature: float = Field(default=1.0, ge=0.0, le=2.0)


class GenerationImageSchema(BaseModel):
    id: int
    file_path: str
    file_size: int
    image_type: str
    index: int

    class Config:
        from_attributes = True


class GenerationSchema(BaseModel):
    id: int
    prompt: str
    aspect_ratio: str
    resolution: str
    thinking_level: str
    temperature: float
    response_text: str | None
    status: str
    error_message: str | None
    created_at: datetime
    completed_at: datetime | None
    images: list[GenerationImageSchema]

    class Config:
        from_attributes = True


class GenerationCreate(BaseModel):
    prompt: str
    config: GenerationConfig = Field(default_factory=GenerationConfig)


class HistoryResponse(BaseModel):
    items: list[GenerationSchema]
    total: int
    page: int
    page_size: int
