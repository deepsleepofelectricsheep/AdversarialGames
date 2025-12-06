from typing import Any


class Agent:
    def action(self, state: Any) -> Any:
        return NotImplementedError()