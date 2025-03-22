# Copyright 2025 Darik Harter
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
# file except in compliance with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied.  See the License for the specific language
# governing permissions and limitations under the License.

import argparse
import readline
import signal
from dataclasses import dataclass

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.spinner import Spinner as RichSpinner

from .base.chat import Chat
from .providers.providers import get_provider, get_providers
from .spinner import Spinner

MULTI_LINE_INPUT = '"""'

_receiving_response = False
_stop_response = False


@dataclass(frozen=True)
class Args:
    command: str
    plain: bool


@dataclass(frozen=True)
class ChatArgs(Args):
    model: str


def sigint_handler(*_):
    """Handle SIGINT (Ctrl+C) to stop the response."""
    global _receiving_response, _stop_response
    if _receiving_response:
        _stop_response = True


def send(chat: Chat, user_input: str, args: ChatArgs) -> None:
    """Send a message to the model and print the response."""
    global _receiving_response, _stop_response
    _receiving_response = True
    _stop_response = False

    try:
        response = chat.send(user_input)

        if args.plain:
            spinner = Spinner()
            for chunk in response:
                spinner.stop()
                if chunk:
                    print(chunk, end="", flush=True)
                if _stop_response:
                    break
            print()
        else:
            full_response = ""
            with Live(console=Console(), refresh_per_second=20) as live:
                live.update(RichSpinner("dots"))
                for chunk in response:
                    if chunk:
                        full_response += chunk
                        live.update(Markdown(full_response))
                    if _stop_response:
                        break
    finally:
        _receiving_response = False
        _stop_response = False


def save_chat(user_input: str, chat: Chat) -> None:
    """Save chat to a file."""
    from .persistence import get_save_file_path, save_chat, save_file_exists

    parts = user_input.split()
    if len(parts) != 2:
        print("Usage:\n  /save <file>")
        return

    if not chat.history:
        print("No chat history to save.")
        return

    filename = parts[1]
    if "/" in filename or "\\" in filename:
        print("Invalid filename.")
        return

    path = get_save_file_path(filename)
    if (
        save_file_exists(filename)
        and input(f"File '{path}' already exists. Overwrite? (y/n) ").strip().lower()
        != "y"
    ):
        return

    try:
        path = save_chat(chat, filename)
        print(f"\nSaved chat to '{path}'.")
    except Exception as e:
        print(f"Error saving chat: {e}")


def load_chat(user_input: str, chat: Chat, args: ChatArgs) -> None:
    """Load chat from a file."""
    from .persistence import load_chat

    parts = user_input.split()
    if len(parts) != 2:
        print("Usage:\n  /load <file>")
        return

    filename = parts[1]

    if chat.history and input("Overwrite current chat? (y/n) ").strip().lower() != "y":
        return

    try:
        load_chat(filename, chat)
        print_chat(chat, args)
    except Exception as e:
        print(f"Error loading chat: {e}")


def print_chat(chat: Chat, args: ChatArgs) -> None:
    """Print the chat history."""
    if not chat.history:
        return

    for message in chat.history:
        if message.from_user():
            print(f"\n[{chat.model}] >>> {message.content}")
        else:
            if args.plain:
                print(message.content)
            else:
                Console().print(Markdown(message.content))


def print_help() -> None:
    """Print help message."""
    print(
        "Available Commands:\n"
        "  /clear            Clear chat history\n"
        "  /save <file>      Save chat to a file\n"
        "  /load <file>      Load chat from a file\n"
        "  /bye              Exit\n"
        "  /?, /help         Print available commands\n"
        "\n"
        f"Use {MULTI_LINE_INPUT} to begin a multi-line message."
    )


def handle_command(user_input: str, chat: Chat, args: ChatArgs) -> None:
    """Handle an user command."""
    command = user_input.split()[0]

    if command == "/bye":
        raise EOFError
    elif command == "/clear":
        chat.clear()
        print("Cleared chat history.")
    elif command == "/load":
        load_chat(user_input, chat, args)
    elif command == "/save":
        save_chat(user_input, chat)
    elif command == "/?" or command == "/help":
        print_help()
    else:
        print(f"Unknown command: '{command}'. Type /? for help.")

    print()


def get_user_input(chat: Chat) -> str:
    """Get user input."""
    user_input = input(f"[{chat.model}] >>> ").strip()

    # Handle multi-line input.
    if user_input.startswith(MULTI_LINE_INPUT):
        lines = [user_input[len(MULTI_LINE_INPUT) :]]
        while True:
            line = input().rstrip()
            if line.endswith(MULTI_LINE_INPUT):
                lines.append(line[: -len(MULTI_LINE_INPUT)])
                break
            lines.append(line)
        user_input = "\n".join(lines).strip()

    return user_input.strip()


def input_loop(chat: Chat, args: ChatArgs) -> None:
    """Run the input loop for the chat session."""
    while True:
        try:
            user_input = get_user_input(chat).strip()
            if not user_input:
                continue
            if user_input.startswith("/"):
                handle_command(user_input, chat, args)
                continue
        except EOFError:
            break

        try:
            send(chat, user_input, args)
        except Exception as e:
            print(f"Error: {e}")

        print()


def split_model(model: str) -> tuple[str, str]:
    """Split a model string into a provider key and model name."""
    parts = model.split(":", maxsplit=1)
    if len(parts) != 2:
        raise ValueError(f"Invalid model: {model}")
    return parts[0], parts[1]


# chat command
def chat(args: ChatArgs) -> None:
    """Start an interactive chat session."""
    # Register SIGINT handler.
    signal.signal(signal.SIGINT, sigint_handler)

    # Enable better line editing.
    readline.parse_and_bind("set editing-mode emacs")

    key, model = split_model(args.model)

    spinner = Spinner()
    try:
        chat = get_provider(key).create_chat(model)
    finally:
        spinner.stop()

    input_loop(chat, args)


def print_markdown(markdown: str, args: Args) -> None:
    """Print a markdown string."""
    if args.plain:
        print(markdown)
    else:
        Console().print(Markdown(markdown))


def get_providers_models_list() -> str:
    """Return a markdown string listing all available models."""
    providers = get_providers()
    if not providers:
        raise RuntimeError("No providers available")

    markdown = "# Available Models"

    for provider in sorted(providers, key=lambda p: p.name):
        markdown += f"\n\n## {provider.name}"

        if provider.api_key is None:
            markdown += (
                f"\n\nAPI key environment variable ({provider.api_key_name}) not set."
            )
            continue

        models = provider.models
        if not models:
            markdown += "\n\nNo models available."
            continue
        for model in sorted(models):
            markdown += f"\n* {provider.key}:{model}"

    return markdown


# list command
def list_models(args: Args) -> None:
    """List available models."""
    print_markdown(get_providers_models_list(), args)


def parse_arguments() -> argparse.Namespace:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Chat with AI in the terminal.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--plain", action="store_true", help="plain text output")

    subparsers = parser.add_subparsers(dest="command", required=True)

    chat_parser = subparsers.add_parser("chat", help="chat with a model")
    chat_parser.add_argument("model", help="the model to use")

    subparsers.add_parser("list", help="list available models")
    subparsers.add_parser("version", help="print version")

    return parser.parse_args()


def get_args() -> ChatArgs | Args:
    """Parse the command-line arguments and return the appropriate Args object."""
    args = parse_arguments()
    if args.command == "chat":
        return ChatArgs(args.command, args.plain, args.model)
    if args.command in ("list", "version"):
        return Args(args.command, args.plain)
    raise ValueError(f"Unknown command: {args.command}")


def main() -> None:
    args = get_args()
    if isinstance(args, ChatArgs):
        chat(args)
    elif args.command == "list":
        list_models(args)
    elif args.command == "version":
        from chai import __version__

        print(f"chai {__version__}")
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
