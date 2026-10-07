import math
from dataclasses import dataclass
from errors import ValidationError

@dataclass(frozen=True)
class Student:
    id: str
    name: str

    def __post_init__(self) -> None:
        if not self.id:
            raise ValidationError("Student id cannot be empty.")
        if not self.name:
            raise ValidationError("Student name cannot be empty.")

@dataclass(frozen=True)
class Assessment:
    id: str
    title: str
    weight: float
    total: float

    def __post_init__(self) -> None:
        if not self.id:
            raise ValidationError("Assessment id cannot be empty.")
        if not self.title:
            raise ValidationError("Assessment title cannot be empty.")
        if not (0 <= self.weight <= 100):
            raise ValidationError("Assessment weight must be between 0 and 100.")
        if self.total <= 0:
            raise ValidationError("Assessment total must be strictly above 0.")

@dataclass(frozen=True)
class Mark:
    student: str
    assessment: str
    score: float

    def __post_init__(self) -> None:
        if self.score < 0:
            raise ValidationError("Mark score cannot be negative.")

def parse_number(raw: object, field: str) -> float:
    if isinstance(raw, bool):
        raise ValidationError(f"{field} must be a number, not a boolean.")
    if isinstance(raw, (int, float, str)):
        try:
            val = float(raw)
        except (ValueError, TypeError):
            raise ValidationError(f"{field} must be a valid number.")
    else:
        raise ValidationError(f"{field} must be a number.")
    
    if not math.isfinite(val):
        raise ValidationError(f"{field} must be a finite number.")
    return val

def parse_text(raw: object, field: str) -> str:
    if not isinstance(raw, str):
        raise ValidationError(f"{field} must be text.")
    val = raw.strip()
    if not val:
        raise ValidationError(f"{field} cannot be blank.")
    return val

def parse_student(payload: object) -> Student:
    if not isinstance(payload, dict):
        raise ValidationError("Student payload must be a JSON object.")
    if "id" not in payload or "name" not in payload:
        raise ValidationError("Student must include 'id' and 'name'.")
    return Student(
        id=parse_text(payload.get("id"), "id"),
        name=parse_text(payload.get("name"), "name")
    )

def parse_assessment(payload: object) -> Assessment:
    if not isinstance(payload, dict):
        raise ValidationError("Assessment payload must be a JSON object.")
    for field in ["id", "title", "weight", "total"]:
        if field not in payload:
            raise ValidationError(f"Assessment must include '{field}'.")
    return Assessment(
        id=parse_text(payload.get("id"), "id"),
        title=parse_text(payload.get("title"), "title"),
        weight=parse_number(payload.get("weight"), "weight"),
        total=parse_number(payload.get("total"), "total")
    )

def parse_mark(payload: object) -> Mark:
    if not isinstance(payload, dict):
        raise ValidationError("Mark payload must be a JSON object.")
    for field in ["student", "assessment", "score"]:
        if field not in payload:
            raise ValidationError(f"Mark must include '{field}'.")
    return Mark(
        student=parse_text(payload.get("student"), "student"),
        assessment=parse_text(payload.get("assessment"), "assessment"),
        score=parse_number(payload.get("score"), "score")
    )