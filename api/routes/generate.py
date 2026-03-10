import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, BackgroundTasks
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Generation, GenerationImage, ImageType
from ..schemas import GenerationSchema
from ..services.storage import save_input_image
from ..services.generation import run_generation

router = APIRouter()


@router.post("/generate", response_model=GenerationSchema)
async def create_generation(
    background_tasks: BackgroundTasks,
    prompt: Annotated[str, Form()],
    aspect_ratio: Annotated[str, Form()] = "1:1",
    resolution: Annotated[str, Form()] = "2K",
    thinking_level: Annotated[str, Form()] = "high",
    temperature: Annotated[float, Form()] = 1.0,
    images: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
):
    """Create a new image generation request."""
    generation = Generation(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        thinking_level=thinking_level,
        temperature=temperature,
    )
    db.add(generation)
    db.commit()
    db.refresh(generation)

    for idx, upload_file in enumerate(images):
        content = await upload_file.read()
        rel_path, file_size = save_input_image(content, upload_file.filename or "image.png")
        db_image = GenerationImage(
            generation_id=generation.id,
            file_path=rel_path,
            file_size=file_size,
            image_type=ImageType.INPUT.value,
            index=idx,
        )
        db.add(db_image)

    db.commit()
    db.refresh(generation)

    background_tasks.add_task(run_generation, db, generation.id)

    return generation
