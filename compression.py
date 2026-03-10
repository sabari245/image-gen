import os
import tempfile
from pathlib import Path

from webptools import cwebp


class WebPCompressor:
    """Handles WebP image compression and conversion."""

    def __init__(self, lossless: bool = True, quality: int = 9, method: int = 6):
        self.lossless = lossless
        self.quality = quality
        self.method = method

    @property
    def _options(self) -> str:
        if self.lossless:
            return f"-lossless -z {self.quality} -m {self.method}"
        return f"-q {self.quality} -m {self.method}"

    def convert(self, input_path: str | Path, output_path: str | Path) -> Path:
        """Convert an image to WebP format."""
        output_path = Path(output_path).with_suffix(".webp")

        result = cwebp(
            input_image=str(input_path),
            output_image=str(output_path),
            option=self._options,
        )
        if result.get("exit_code") != 0:
            raise RuntimeError(result.get("stderr", "Unknown error"))

        return output_path

    def convert_bytes(self, data: bytes, output_path: str | Path) -> Path:
        """Convert raw image bytes to WebP format."""
        output_path = Path(output_path).with_suffix(".webp")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        try:
            result = cwebp(
                input_image=tmp_path,
                output_image=str(output_path),
                option=self._options,
            )
            if result.get("exit_code") != 0:
                raise RuntimeError(result.get("stderr", "Unknown error"))
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        return output_path

    def convert_to_temp(self, input_path: str | Path) -> Path:
        """Convert an image to a temporary WebP file."""
        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        result = cwebp(
            input_image=str(input_path),
            output_image=str(tmp_path),
            option=self._options,
        )
        if result.get("exit_code") != 0:
            raise RuntimeError(result.get("stderr", "Unknown error"))

        return tmp_path

    @staticmethod
    def get_compression_ratio(original_path: str | Path, compressed_path: str | Path) -> float:
        """Calculate compression savings percentage."""
        original_size = os.path.getsize(original_path)
        compressed_size = os.path.getsize(compressed_path)
        return (1 - compressed_size / original_size) * 100
