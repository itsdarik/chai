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

from typing import Generator

from google import genai
from google.genai.types import Content, Part

from ..base.chat import Chat
from ..base.message import Message
from ..base.provider import Provider


class GoogleChat(Chat):
    """Google chat session."""

    def __init__(self, api_key: str, model: str) -> None:
        super().__init__(model)
        self._client: genai.Client = genai.Client(api_key=api_key)
        self._chat = self._client.chats.create(model=model)

    def _send(self, message: str) -> Generator[str, None, None]:
        for chunk in self._chat.send_message_stream(message):
            content = chunk.text
            if content:
                yield content

    def clear(self) -> None:
        super().clear()
        self._chat = self._client.chats.create(model=self._model)

    def load(self, history: list[Message]) -> None:
        super().load(history)
        chat_history = []
        for message in history:
            role = "model" if message.role == "assistant" else message.role
            chat_history.append(Content(parts=[Part(text=message.content)], role=role))
        self._chat = self._client.chats.create(model=self._model, history=chat_history)


class GoogleProvider(Provider):
    """Google provider."""

    def __init__(self) -> None:
        super().__init__("Google", "GOOGLE_API_KEY")

    def _get_models(self) -> list[str]:
        return sorted(
            [
                model.name.removeprefix("models/")
                for model in genai.Client(api_key=self.api_key).models.list()
            ]
        )

    def _create_chat_instance(self, model: str) -> GoogleChat:
        return GoogleChat(self.api_key, model)
