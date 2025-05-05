from google import genai
from google.genai import types


def get_models() -> list[types.Model]:
    """Return the available Gemini models."""
    try:
        return sorted(genai.Client().models.list(), key=lambda model: model.name or "")
    except Exception as e:
        raise RuntimeError(f"Error listing models: {e}") from e
