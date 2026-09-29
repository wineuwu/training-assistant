import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

import main
from main import TrainingCreate, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage():
    main.trainings.clear()
    main.next_id = 1


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_running_without_menu():
    t = TrainingCreate(date="2026-03-26", type="running", duration=40)
    assert t.menu is None


def test_strength_with_menu():
    t = TrainingCreate(
        date="2026-03-26", type="strength", duration=40, menu="snatch 35kg x 5reps x 4 "
    )

    assert t.menu is not None


def test_hiit_without_menu():
    with pytest.raises(ValidationError):
        TrainingCreate(date="2026-03-26", type="hiit", duration=40)


def test_badminton_with_menu():
    with pytest.raises(ValidationError):
        TrainingCreate(date="2026-03-26", type="badminton", menu="週四", duration=40)


def test_create_training():
    response = client.post(
        "/trainings",
        json={"date": "2026-03-26", "type": "running", "duration": 40},
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["duration"] == 40


def test_id_increments():
    post1 = client.post(
        "/trainings",
        json={"date": "2026-03-26", "type": "running", "duration": 40},
    )
    post2 = client.post(
        "/trainings",
        json={
            "date": "2026-03-26",
            "type": "emom",
            "duration": 40,
            "menu": "burpee x 20",
        },
    )

    assert post1.status_code == 201
    assert post1.json()["id"] == 1
    assert post2.status_code == 201
    assert post2.json()["id"] == 2


def test_list_trainings():
    post_training = client.post(
        "/trainings",
        json={"date": "2026-03-26", "type": "running", "duration": 40},
    )

    assert post_training.status_code == 201

    response = client.get("/trainings")
    d = response.json()
    assert len(d) == 1


def test_get_training_not_found():

    post_training = client.post(
        "/trainings",
        json={"date": "2026-03-26", "type": "running", "duration": 40},
    )

    assert post_training.status_code == 201

    training_list = client.get("/trainings/3")

    assert training_list.status_code == 404


def test_get_trainings():
    post_training = client.post(
        "/trainings",
        json={"date": "2026-03-26", "type": "running", "duration": 40},
    )

    assert post_training.status_code == 201

    training = client.get("/trainings/1")

    assert training.status_code == 200
    assert training.json()["id"] == 1


def test_update_training():
    post1 = client.post(
        "/trainings", json={"date": "2026-03-26", "type": "running", "duration": 40}
    )

    assert post1.status_code == 201

    put_id_1 = client.put(
        "/trainings/1", json={"date": "2026-03-26", "type": "running", "duration": 60}
    )
    assert put_id_1.status_code == 200
    assert put_id_1.json()["duration"] == 60
    assert put_id_1.json()["id"] == 1


def test_update_not_found():
    res = client.put(
        "/trainings/999", json={"date": "2026-03-26", "type": "running", "duration": 40}
    )
    assert res.status_code == 404
