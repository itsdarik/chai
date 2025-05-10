import typing

import typer

from .commands.chat import chat as _chat
from .commands.list import list_models
from .commands.version import __version__

app = typer.Typer(
    help="Chat with Google DeepMind Gemini models in the terminal.",
    no_args_is_help=True,
    add_completion=False,
)


@app.command("chat", help="Chat with Gemini.", epilog="Use `chai list` to list models.")
def chat(
    model: typing.Annotated[str, typer.Argument(help="Model to chat with.")],
):
    if not model.startswith("models/"):
        model = f"models/{model}"
    _chat(model=model)


@app.command("list", help="List Gemini models.")
def list():
    list_models()


def _print_version():
    print(f"chai {__version__}")


@app.command("version", help="Print the chai version.")
def version():
    _print_version()
