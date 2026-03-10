import os
from pathlib import Path

import click
from dotenv import load_dotenv

from compression import WebPCompressor
from gemini import (
    AspectRatio,
    GenerationConfig,
    GeminiImageGenerator,
    Resolution,
    ThinkingLevel,
)


load_dotenv(Path(".env.local"))


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
    type=click.Choice(["minimal", "high"], case_sensitive=False),
    default="high",
    show_default=True,
    help="Thinking level for generation",
)
@click.option(
    "--aspect-ratio",
    type=click.Choice(
        ["1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9"],
        case_sensitive=False,
    ),
    default="1:1",
    show_default=True,
    help="Output image aspect ratio",
)
@click.option(
    "--resolution",
    type=click.Choice(["512", "1K", "2K", "4K"], case_sensitive=False),
    default="2K",
    show_default=True,
    help="Output image resolution",
)
@click.option(
    "--temperature",
    type=float,
    default=1.0,
    show_default=True,
    help="Temperature for generation (0.0-2.0)",
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
    temperature: float,
    output: str,
):
    """Generate images using Gemini API."""
    try:
        generator = GeminiImageGenerator()
    except ValueError as e:
        raise click.ClickException(str(e))

    config = GenerationConfig(
        aspect_ratio=AspectRatio(aspect_ratio),
        resolution=Resolution(resolution),
        thinking_level=ThinkingLevel(thinking_level.lower()),
        temperature=temperature,
    )

    if images:
        click.echo(f"Processing {len(images)} input image(s)...")

    click.echo("Generating...")

    result = generator.generate(
        prompt=prompt,
        images=list(images),
        config=config,
    )

    compressor = WebPCompressor()

    for img in result.images:
        file_name = f"{output}_{img.index}"
        webp_path = compressor.convert_bytes(img.data, file_name)
        file_size = os.path.getsize(webp_path)
        size_kb = file_size / 1024
        click.echo(f"Saved: {webp_path} ({size_kb:.1f}KB)")

    if result.text:
        click.echo(result.text)

    if not result.images:
        click.echo("No images generated.")

    click.echo("Done!")


if __name__ == "__main__":
    generate()
