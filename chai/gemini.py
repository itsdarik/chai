from collections.abc import Iterator

from google import genai
from google.genai import types


def list_models() -> Iterator[types.Model]:
    """List available Gemini models."""
    client = genai.Client()
    try:
        yield from client.models.list()
    except Exception as e:
        raise RuntimeError(f"Error listing models: {e}") from e
