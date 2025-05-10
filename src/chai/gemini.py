from google import genai
from google.genai import types
from google.genai.chats import Chat


def _get_client() -> genai.Client:
    """Return a client for the Gemini API."""
    try:
        return genai.Client()
    except Exception as e:
        raise RuntimeError(f"Error creating client: {e}") from e


def get_models() -> list[types.Model]:
    """Return the available Gemini models."""
    try:
        return sorted(_get_client().models.list(), key=lambda model: model.name or "")
    except Exception as e:
        raise RuntimeError(f"Error listing models: {e}") from e


def get_chat(model: str) -> Chat:
    """Return a chat for the given model."""
    try:
        return _get_client().chats.create(model=model)
    except Exception as e:
        raise RuntimeError(f"Error creating chat: {e}") from e
