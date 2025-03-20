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

import json
from pathlib import Path

from .base.chat import Chat
from .base.message import Message

SAVE_DIR = Path.home() / ".chai"


def get_save_file_path(filename: str) -> Path:
    """Return the full path for a save file."""
    if not filename.endswith(".json"):
        filename += ".json"
    return SAVE_DIR / filename


def ensure_save_dir() -> None:
    """Ensure save directory exists."""
    SAVE_DIR.mkdir(parents=True, exist_ok=True)


def serialize_conversation(chat: Chat) -> dict[str, any]:
    """Serialize a chat conversation to a dictionary."""
    return {
        "model": chat.model,
        "messages": [message.to_dict() for message in chat.history],
    }


def save_file_exists(filename: str) -> bool:
    """Check if a save file exists."""
    return get_save_file_path(filename).exists()


def save_chat(chat: Chat, filename: str) -> Path:
    """Save a conversation to a file.

    Returns the path to the file.
    """
    path = get_save_file_path(filename)
    ensure_save_dir()

    with open(path, "w") as save_file:
        json.dump(serialize_conversation(chat), save_file, indent=4)

    return path


def load_chat(filename: str, chat: Chat) -> None:
    """Load a conversation from a file into an existing chat."""
    path = get_save_file_path(filename)

    if not path.exists():
        raise FileNotFoundError(f"File '{path}' does not exist.")

    with open(path) as save_file:
        conversation = json.load(save_file)

    if "model" not in conversation:
        raise ValueError(f"model not found in file '{path}'.")

    if "messages" not in conversation:
        raise ValueError(f"messages not found in file '{path}'.")

    if conversation["model"] != chat.model:
        raise ValueError(
            f"model in file '{path}' ({conversation['model']}) does not match current model ({chat.model})."
        )

    chat.load([Message.from_dict(message) for message in conversation["messages"]])
