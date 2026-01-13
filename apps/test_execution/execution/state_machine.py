"""State machine helpers for test runs (placeholder)."""


class TestRunStateMachine:
    def __init__(self, current_state: str):
        self.current_state = current_state

    def can_transition_to(self, target_state: str) -> bool:
        return True

