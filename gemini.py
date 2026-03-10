import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from compression import WebPCompressor


class AspectRatio(str, Enum):
    """Supported aspect ratios for Gemini image generation."""

    RATIO_1_1 = "1:1"
    RATIO_1_4 = "1:4"
    RATIO_1_8 = "1:8"
    RATIO_2_3 = "2:3"
    RATIO_3_2 = "3:2"
    RATIO_3_4 = "3:4"
    RATIO_4_1 = "4:1"
    RATIO_4_3 = "4:3"
    RATIO_4_5 = "4:5"
    RATIO_5_4 = "5:4"
    RATIO_8_1 = "8:1"
    RATIO_9_16 = "9:16"
    RATIO_16_9 = "16:9"
    RATIO_21_9 = "21:9"


class Resolution(str, Enum):
    """Supported resolutions for Gemini image generation."""

    RES_512 = "512"
    RES_1K = "1K"
    RES_2K = "2K"
    RES_4K = "4K"


class ThinkingLevel(str, Enum):
    """Thinking levels for gemini-3.1-flash-image-preview model."""

    MINIMAL = "minimal"
    HIGH = "high"


class GenerationConfig(BaseModel):
    """Configuration for image generation."""

    aspect_ratio: AspectRatio = Field(default=AspectRatio.RATIO_1_1)
    resolution: Resolution = Field(default=Resolution.RES_2K)
    thinking_level: ThinkingLevel = Field(default=ThinkingLevel.HIGH)
    temperature: float = Field(default=1.0, ge=0.0, le=2.0)


@dataclass
class GeneratedImage:
    """Represents a generated image."""

    data: bytes
    index: int


@dataclass
class GenerationResult:
    """Result of image generation."""

    images: list[GeneratedImage]
    text: str


class GeminiImageGenerator:
    """Handles image generation using Gemini API."""

    MODEL = "gemini-3.1-flash-image-preview"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=self.api_key)
        self.compressor = WebPCompressor()

    def upload_image(self, image_path: str | Path) -> types.File:
        """Upload an image to Gemini API, converting to WebP if needed."""
        image_path = Path(image_path)

        if image_path.suffix.lower() == ".webp":
            return self.client.files.upload(file=str(image_path))

        tmp_path = self.compressor.convert_to_temp(image_path)
        try:
            uploaded_file = self.client.files.upload(file=str(tmp_path))
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

        return uploaded_file

    def generate(
        self,
        prompt: str,
        images: list[str | Path] | None = None,
        config: GenerationConfig | None = None,
    ) -> GenerationResult:
        """Generate images from a prompt and optional input images."""
        config = config or GenerationConfig()
        images = images or []

        parts = []

        for image_path in images:
            uploaded_file = self.upload_image(image_path)
            parts.append(
                types.Part.from_uri(
                    file_uri=uploaded_file.uri,
                    mime_type=uploaded_file.mime_type,
                )
            )

        parts.append(types.Part.from_text(text=prompt))

        contents = [
            types.Content(
                role="user",
                parts=parts,
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level=config.thinking_level.value,
            ),
            image_config=types.ImageConfig(
                aspect_ratio=config.aspect_ratio.value,
                image_size=config.resolution.value,
            ),
            temperature=config.temperature,
            response_modalities=[
                "IMAGE",
                "TEXT",
            ],
        )

        generated_images = []
        text_parts = []
        image_index = 0

        for chunk in self.client.models.generate_content_stream(
            model=self.MODEL,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.parts is None:
                continue

            for part in chunk.parts:
                if part.inline_data and part.inline_data.data:
                    generated_images.append(
                        GeneratedImage(data=part.inline_data.data, index=image_index)
                    )
                    image_index += 1
                elif part.text:
                    text_parts.append(part.text)

        return GenerationResult(
            images=generated_images,
            text="".join(text_parts),
        )
