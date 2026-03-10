import asyncio
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from gemini import GeminiImageGenerator, GenerationConfig, AspectRatio, Resolution, ThinkingLevel
from ..models import Generation, GenerationImage, GenerationStatus, ImageType
from .storage import save_output_image, get_image_path


def get_aspect_ratio(value: str) -> AspectRatio:
    for ar in AspectRatio:
        if ar.value == value:
            return ar
    return AspectRatio.RATIO_1_1


def get_resolution(value: str) -> Resolution:
    for r in Resolution:
        if r.value == value:
            return r
    return Resolution.RES_2K


def get_thinking_level(value: str) -> ThinkingLevel:
    for tl in ThinkingLevel:
        if tl.value == value:
            return tl
    return ThinkingLevel.HIGH


async def run_generation(db: Session, generation_id: int):
    """Run the actual image generation in a background task."""
    generation = db.query(Generation).filter(Generation.id == generation_id).first()
    if not generation:
        return

    generation.status = GenerationStatus.PROCESSING.value
    db.commit()

    try:
        generator = GeminiImageGenerator()

        config = GenerationConfig(
            aspect_ratio=get_aspect_ratio(generation.aspect_ratio),
            resolution=get_resolution(generation.resolution),
            thinking_level=get_thinking_level(generation.thinking_level),
            temperature=generation.temperature,
        )

        input_images = [
            get_image_path(img.file_path)
            for img in generation.images
            if img.image_type == ImageType.INPUT.value
        ]

        result = await asyncio.to_thread(
            generator.generate,
            generation.prompt,
            input_images,
            config,
        )

        for idx, gen_image in enumerate(result.images):
            rel_path, file_size = save_output_image(gen_image.data, generation_id, idx)
            db_image = GenerationImage(
                generation_id=generation_id,
                file_path=rel_path,
                file_size=file_size,
                image_type=ImageType.OUTPUT.value,
                index=idx,
            )
            db.add(db_image)

        generation.response_text = result.text
        generation.status = GenerationStatus.COMPLETED.value
        generation.completed_at = datetime.utcnow()
        db.commit()

    except Exception as e:
        generation.status = GenerationStatus.FAILED.value
        generation.error_message = str(e)
        generation.completed_at = datetime.utcnow()
        db.commit()
