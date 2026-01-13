"""Event payload definitions (placeholder)."""


def test_run_payload(test_run_id: int, status: str) -> dict:
    return {"id": test_run_id, "status": status}

