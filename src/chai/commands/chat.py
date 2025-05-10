import dataclasses
import typing

from google.genai.chats import Chat
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.markup import MarkdownLexer

from ..gemini import get_chat, get_models


@dataclasses.dataclass(frozen=True)
class ChatSession:
    prompt: PromptSession
    chat: Chat


def _validate_model(model: str):
    """Ensure a model is an available Gemini model."""
    models = [model.name for model in get_models()]
    if model not in models:
        raise ValueError(f"{model=} not found. Available {models=}")


def _get_user_input(model: str, session: PromptSession) -> str:
    """Get user input."""
    user_input = session.prompt(
        f"[{model.removeprefix('models/')}] >>> ",
        lexer=PygmentsLexer(MarkdownLexer),
        multiline=True,
        prompt_continuation="... ",
        wrap_lines=False,
    )
    if not isinstance(user_input, str):
        raise ValueError(f"{user_input=} is not a string")
    return user_input.strip()


def _get_response(chat: Chat, prompt: str) -> typing.Generator[str]:
    """Get a response from the Gemini API."""
    for chunk in chat.send_message_stream(message=prompt):
        content = chunk.text
        if content:
            yield content


def _chat(model: str):
    """Main chat loop."""
    chat_session: ChatSession = ChatSession(
        chat=get_chat(model=model), prompt=PromptSession()
    )
    while True:
        try:
            user_input = _get_user_input(model=model, session=chat_session.prompt)
            for chunk in _get_response(chat=chat_session.chat, prompt=user_input):
                print(chunk, end="", flush=True)
            print()
        except KeyboardInterrupt:
            continue
        except EOFError:
            break


def chat(model: str):
    """Chat with a Gemini model."""
    _validate_model(model)
    _chat(model)
