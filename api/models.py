from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class GenerationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ImageType(str, Enum):
    INPUT = "input"
    OUTPUT = "output"


class Generation(Base):
    __tablename__ = "generations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    aspect_ratio: Mapped[str] = mapped_column(String(10), default="1:1")
    resolution: Mapped[str] = mapped_column(String(10), default="2K")
    thinking_level: Mapped[str] = mapped_column(String(10), default="high")
    temperature: Mapped[float] = mapped_column(Float, default=1.0)
    response_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default=GenerationStatus.PENDING.value)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    images: Mapped[list["GenerationImage"]] = relationship(
        "GenerationImage", back_populates="generation", cascade="all, delete-orphan"
    )


class GenerationImage(Base):
    __tablename__ = "generation_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    generation_id: Mapped[int] = mapped_column(Integer, ForeignKey("generations.id"), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, default=0)
    image_type: Mapped[str] = mapped_column(String(10), nullable=False)
    index: Mapped[int] = mapped_column(Integer, default=0)

    generation: Mapped["Generation"] = relationship("Generation", back_populates="images")
