from datetime import date
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, model_validator


class TrainingType(str, Enum):
    badminton = "badminton"
    running = "running"
    hiit = "hiit"
    emom = "emom"
    strength = "strength"
    mixed = "mixed"


class Effort(str, Enum):
    almost_die = "almost_die"
    very_hard = "very_hard"
    hard = "hard"
    normal = "normal"
    easy = "easy"


NEEDS_MENU_ITEMS = {
    TrainingType.hiit,
    TrainingType.emom,
    TrainingType.strength,
    TrainingType.mixed,
}


class TrainingCreate(BaseModel):
    date: date
    type: TrainingType
    duration: int
    menu: str | None = None
    distance: float | None = None
    average_heart_rate: int | None = None
    effort: Effort | None = None
    note: str | None = None

    @model_validator(mode="after")
    def validate_menu(self):

        needs_menu = self.type in NEEDS_MENU_ITEMS
        has_menu = bool(self.menu)

        if needs_menu and not has_menu:
            raise ValueError(f"{self.type.value} 需要填寫今日訓練菜單")
        if not needs_menu and has_menu:
            raise ValueError(f"{self.type.value} 不需要填寫今日訓練菜單")

        return self


class Training(TrainingCreate):
    id: int


trainings: list[Training] = []
next_id = 1


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/trainings", status_code=201, response_model=Training)
def create_training(payload: TrainingCreate):
    global next_id
    record = Training(id=next_id, **payload.model_dump())
    next_id += 1
    trainings.append(record)
    return record
