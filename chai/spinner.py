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

import itertools
import threading
import time

SPINNER_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
FRAMES_PER_SECOND = 10


class Spinner:
    def __init__(self):
        self._running = True
        self._thread = threading.Thread(target=self._spin)
        self._thread.start()

    def _spin(self):
        """Animate the spinner."""
        while self._running:
            for char in itertools.cycle(SPINNER_CHARS):
                if not self._running:
                    return
                print(f"\r{char} ", end="", flush=True)
                time.sleep(1 / FRAMES_PER_SECOND)

    def stop(self):
        """Stop the spinner."""
        if not self._running:
            return
        self._running = False
        self._thread.join()
        print("\r", end="", flush=True)
