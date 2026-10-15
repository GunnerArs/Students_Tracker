"""Student Tracker: models, business logic and CSV persistence."""

from __future__ import annotations

import csv
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Student:
    name: str
    age: int
    math: float
    literature: float
    english: float
    student_id: Optional[int] = None

    @property
    def average(self) -> float:
        return round((self.math + self.literature + self.english) / 3, 2)

    @property
    def ranking(self) -> str:
        avg = self.average
        if avg >= 8.0:
            return "Giỏi"
        if avg >= 6.5:
            return "Khá"
        if avg >= 5.0:
            return "Trung bình"
        return "Yếu"

    def display(self) -> str:
        id_part = f"[{self.student_id}] " if self.student_id is not None else ""
        return f"{id_part}{self.name} | Tuổi: {self.age} | ĐTB: {self.average:.2f} | Xếp loại: {self.ranking}"


class StudentManager:
    def __init__(self, students: Optional[list[Student]] = None) -> None:
        self.students: list[Student] = list(students or [])

    def add(self, student: Student) -> None:
        self.students.append(student)

    def find_by_name(self, keyword: str) -> list[Student]:
        key = keyword.strip().lower()
        return [s for s in self.students if key in s.name.lower()]

    def sort_by_average(self, reverse: bool = True) -> list[Student]:
        return sorted(self.students, key=lambda s: s.average, reverse=reverse)

    def class_average(self) -> float:
        if not self.students:
            return 0.0
        return round(sum(s.average for s in self.students) / len(self.students), 2)


class Repository:
    FIELDS = ("id", "name", "age", "math", "literature", "english")

    def __init__(self, csv_path: str = "students.csv") -> None:
        self.path = Path(csv_path)
        if not self.path.exists():
            self._write([])
        else:
            students = self.list_all()
            if any(student.student_id != index for index, student in enumerate(students, 1)):
                self._renumber(students)
                self._write(students)

    @staticmethod
    def _renumber(students: list[Student]) -> None:
        for index, student in enumerate(students, 1):
            student.student_id = index

    def _read(self) -> list[Student]:
        with self.path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != list(self.FIELDS):
                raise ValueError(f"CSV không đúng cột: {self.path}")
            return [Student(
                name=row["name"], age=int(row["age"]), math=float(row["math"]),
                literature=float(row["literature"]), english=float(row["english"]),
                student_id=int(row["id"]),
            ) for row in reader]

    def _write(self, students: list[Student]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path: str | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8-sig", newline="", dir=self.path.parent,
                prefix=".students-", suffix=".csv", delete=False,
            ) as stream:
                temp_path = stream.name
                writer = csv.DictWriter(stream, fieldnames=self.FIELDS)
                writer.writeheader()
                for student in students:
                    writer.writerow({
                        "id": student.student_id, "name": student.name, "age": student.age,
                        "math": student.math, "literature": student.literature, "english": student.english,
                    })
            os.replace(temp_path, self.path)
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)

    def list_all(self) -> list[Student]:
        return sorted(self._read(), key=lambda student: student.student_id or 0)

    def load_manager(self) -> StudentManager:
        return StudentManager(self.list_all())

    def add(self, student: Student) -> int:
        students = self._read()
        student.student_id = len(students) + 1
        students.append(student)
        self._write(students)
        return student.student_id

    def add_missing(self, candidates: list[Student]) -> int:
        """Import only records whose student details are not already in the CSV."""
        students = self._read()
        def details(student: Student) -> tuple[str, int, float, float, float]:
            return (student.name, student.age, student.math,
                    student.literature, student.english)

        known = {details(student) for student in students}
        next_id = len(students)
        added = 0
        for candidate in candidates:
            key = details(candidate)
            if key in known:
                continue
            next_id += 1
            candidate.student_id = next_id
            students.append(candidate)
            known.add(key)
            added += 1
        if added:
            self._write(students)
        return added

    def update(self, student: Student) -> None:
        if student.student_id is None:
            raise ValueError("Cần có student_id để sửa.")
        students = self._read()
        for index, existing in enumerate(students):
            if existing.student_id == student.student_id:
                students[index] = student
                self._write(students)
                return

    def delete(self, student_id: int) -> bool:
        students = self._read()
        remaining = [student for student in students if student.student_id != student_id]
        if len(remaining) == len(students):
            return False
        self._renumber(remaining)
        self._write(remaining)
        return True

    def get(self, student_id: int) -> Optional[Student]:
        return next((student for student in self._read() if student.student_id == student_id), None)

    def close(self) -> None:
        pass
