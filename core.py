"""Student Tracker: models, business logic and SQLite persistence."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
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
    SCHEMA = """CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        math REAL NOT NULL,
        literature REAL NOT NULL,
        english REAL NOT NULL
    )"""

    def __init__(self, db_path: str = "students.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        with self.conn:
            self.conn.execute(self.SCHEMA)
            self._renumber()

    def _renumber(self) -> None:
        """Fill ID gaps in ascending order, inside the caller's transaction."""
        ids = [row[0] for row in self.conn.execute("SELECT id FROM students ORDER BY id")]
        for new_id, old_id in enumerate(ids, 1):
            if new_id != old_id:
                self.conn.execute("UPDATE students SET id=? WHERE id=?", (new_id, old_id))

    @staticmethod
    def _row_to_student(row: sqlite3.Row) -> Student:
        return Student(row["name"], row["age"], row["math"],
                       row["literature"], row["english"], row["id"])

    def list_all(self) -> list[Student]:
        return [self._row_to_student(row) for row in
                self.conn.execute("SELECT * FROM students ORDER BY id")]

    def load_manager(self) -> StudentManager:
        return StudentManager(self.list_all())

    def add(self, student: Student) -> int:
        with self.conn:
            student.student_id = self.conn.execute(
                "SELECT COALESCE(MAX(id), 0) + 1 FROM students"
            ).fetchone()[0]
            self.conn.execute(
                "INSERT INTO students (id, name, age, math, literature, english) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (student.student_id, student.name, student.age, student.math,
                 student.literature, student.english),
            )
        return student.student_id

    def add_missing(self, candidates: list[Student]) -> int:
        """Import only records whose student details are not already in SQLite."""
        def details(student: Student) -> tuple[str, int, float, float, float]:
            return (student.name, student.age, student.math,
                    student.literature, student.english)

        known = {details(student) for student in self.list_all()}
        added = 0
        with self.conn:
            next_id = self.conn.execute("SELECT COALESCE(MAX(id), 0) FROM students").fetchone()[0]
            for candidate in candidates:
                key = details(candidate)
                if key in known:
                    continue
                next_id += 1
                candidate.student_id = next_id
                self.conn.execute(
                    "INSERT INTO students (id, name, age, math, literature, english) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (next_id, candidate.name, candidate.age, candidate.math,
                     candidate.literature, candidate.english),
                )
                known.add(key)
                added += 1
        return added

    def update(self, student: Student) -> None:
        if student.student_id is None:
            raise ValueError("Cần có student_id để sửa.")
        with self.conn:
            self.conn.execute(
                "UPDATE students SET name=?, age=?, math=?, literature=?, english=? WHERE id=?",
                (student.name, student.age, student.math, student.literature,
                 student.english, student.student_id),
            )

    def delete(self, student_id: int) -> bool:
        with self.conn:
            deleted = self.conn.execute(
                "DELETE FROM students WHERE id=?", (student_id,)
            ).rowcount > 0
            if deleted:
                self._renumber()
        return deleted

    def get(self, student_id: int) -> Optional[Student]:
        row = self.conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
        return self._row_to_student(row) if row else None

    def close(self) -> None:
        self.conn.close()
