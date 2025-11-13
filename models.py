from datetime import date
from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    full_name: str
    birth_date: date
    gender: str
    id: Optional[int] = None

    def calculate_age(self) -> int:
        today = date.today()
        age = today.year - self.birth_date.year

        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1

        return age

    def to_dict(self) -> dict:
        return {
            "full_name": self.full_name,
            "birth_date": self.birth_date.isoformat(),
            "gender": self.gender
        }
