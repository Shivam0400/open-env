from pydantic import BaseModel
from typing import Optional, Any, Dict

class Action(BaseModel):
    query: str
    submit_answer: Optional[str] = None

class Observation(BaseModel):
    result: str
    error: Optional[str] = None

class State(BaseModel):
    current_task: int
    task_level: str
    score: float
    is_done: bool

class Reward(BaseModel):
    value: float
    reason: Optional[str] = None

