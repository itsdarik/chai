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

from mistralai import Mistral

from ..base.chat import Chat
from ..base.provider import Provider


class MistralChat(Chat):
    """Mistral chat session."""

    def __init__(self, api_key: str, model: str) -> None:
        super().__init__(model)
        self._client: Mistral = Mistral(api_key=api_key)

    def _send(self, _: str) -> Generator[str, None, None]:
        response = self._client.chat.stream(
            model=self._model,
            messages=[message.to_dict() for message in self._history],
        )

        for chunk in response:
            content = chunk.data.choices[0].delta.content
            if content:
                yield content


class MistralProvider(Provider):
    """Mistral provider."""

    def __init__(self) -> None:
        super().__init__("Mistral", "MISTRAL_API_KEY")

    def _get_models(self) -> list[str]:
        with Mistral(api_key=self.api_key) as mistral:
            return sorted([model.id for model in mistral.models.list().data])

    def _create_chat_instance(self, model: str) -> MistralChat:
        return MistralChat(self.api_key, model)
