import mimetypes
import os
import tempfile
from pathlib import Path

import click
import oxipng
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv(Path(".env/.env"))


def save_binary_file(file_name: str, data: bytes) -> None:
    with open(file_name, "wb") as f:
        f.write(data)

    if file_name.lower().endswith(".png"):
        try:
            oxipng.optimize(file_name, level=6)
        except Exception:
            pass

    file_size = os.path.getsize(file_name)
    size_mb = file_size / 1024 / 1024
    click.echo(f"Saved: {file_name} ({size_mb:.1f}MB)")


def upload_image(client: genai.Client, image_path: str) -> types.File:
    file_ext = Path(image_path).suffix.lower()

    if file_ext == ".png":
        click.echo(f"Compressing: {image_path}")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            import shutil

            shutil.copy2(image_path, tmp_path)
            oxipng.optimize(tmp_path, level=6)
            compressed_size = os.path.getsize(tmp_path)
            original_size = os.path.getsize(image_path)
            saved_pct = (1 - compressed_size / original_size) * 100
            click.echo(f"Compressed: {saved_pct:.1f}% smaller")

            click.echo(f"Uploading: {image_path}")
            uploaded_file = client.files.upload(file=tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    else:
        click.echo(f"Uploading: {image_path}")
        uploaded_file = client.files.upload(file=image_path)

    return uploaded_file


@click.command()
@click.option("--prompt", "-p", required=True, help="Text prompt for image generation")
@click.option(
    "--image",
    "-i",
    "images",
    multiple=True,
    type=click.Path(exists=True),
    help="Input image path (can be used multiple times)",
)
@click.option(
    "--thinking-level",
    type=click.Choice(["LOW", "MEDIUM", "HIGH"], case_sensitive=True),
    default="HIGH",
    show_default=True,
    help="Thinking level for generation",
)
@click.option(
    "--aspect-ratio",
    type=click.Choice(["1:1", "16:9", "9:16", "4:3", "3:4"], case_sensitive=False),
    default="1:1",
    show_default=True,
    help="Output image aspect ratio",
)
@click.option(
    "--resolution",
    type=click.Choice(["256", "512", "1024", "2K"], case_sensitive=False),
    default="2K",
    show_default=True,
    help="Output image resolution",
)
@click.option(
    "--output",
    "-o",
    default="generated",
    show_default=True,
    help="Output filename prefix",
)
def generate(
    prompt: str,
    images: tuple,
    thinking_level: str,
    aspect_ratio: str,
    resolution: str,
    output: str,
):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise click.ClickException("GEMINI_API_KEY not found in .env/.env")

    client = genai.Client(api_key=api_key)

    model = "gemini-3.1-flash-image-preview"

    parts = []

    for image_path in images:
        uploaded_file = upload_image(client, image_path)
        parts.append(
            types.Part.from_uri(
                file_uri=uploaded_file.uri, mime_type=uploaded_file.mime_type
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
            thinking_level=thinking_level,
        ),
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution,
        ),
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
    )

    click.echo("Generating...")

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.parts is None:
            continue

        for part in chunk.parts:
            if part.inline_data and part.inline_data.data:
                file_extension = (
                    mimetypes.guess_extension(part.inline_data.mime_type) or ".png"
                )
                file_name = f"{output}_{file_index}{file_extension}"
                file_index += 1
                save_binary_file(file_name, part.inline_data.data)
            elif part.text:
                click.echo(part.text, nl=False)

    if file_index == 0:
        click.echo("No images generated.")

    click.echo("\nDone!")


if __name__ == "__main__":
    generate()
