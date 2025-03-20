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

import os
from abc import ABC, abstractmethod

from .chat import Chat


class Provider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, name: str, api_key_name: str):
        self._name = name
        self._api_key_name = api_key_name

    @property
    def name(self) -> str:
        """The provider name."""
        return self._name

    @property
    def key(self) -> str:
        """The provider key, which is the lowercase provider name with spaces replaced by dashes."""
        return self._name.lower().replace(" ", "-")

    @property
    def api_key_name(self) -> str:
        """The name of the environment variable that holds the API key."""
        return self._api_key_name

    @property
    def api_key(self) -> str | None:
        """The API key, or None if not set."""
        return os.getenv(self._api_key_name)

    @property
    def models(self) -> list[str]:
        """The list of available models."""
        if self.api_key is None:
            raise RuntimeError(f"{self.api_key_name} environment variable not set")
        try:
            return self._get_models()
        except Exception as e:
            raise RuntimeError(f"Error getting models: {e}")

    @abstractmethod
    def _get_models(self) -> list[str]:
        """Return the provider-specific list of available models."""
        pass

    def create_chat(self, model: str) -> Chat:
        """Create a new chat session."""
        if model not in self.models:
            raise ValueError(f"Invalid model: {model}")
        if self.api_key is None:
            raise RuntimeError(f"{self.api_key_name} environment variable not set")
        return self._create_chat_instance(model)

    @abstractmethod
    def _create_chat_instance(self, model: str) -> Chat:
        """Create the provider-specific chat instance."""
        pass
