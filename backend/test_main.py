import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from main import Training, app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_running_without_menu():
    t = Training(date="2026-03-26", type="running", duration=40)
    assert t.menu is None


def test_strength_with_menu():
    t = Training(
        date="2026-03-26", type="strength", duration=40, menu="snatch 35kg x 5reps x 4 "
    )

    assert t.menu is not None


def test_hiit_without_menu():
    with pytest.raises(ValidationError):
        Training(date="2026-03-26", type="hiit", duration=40)


def test_badminton_with_menu():
    with pytest.raises(ValidationError):
        Training(date="2026-03-26", type="badminton", menu="週四", duration=40)
