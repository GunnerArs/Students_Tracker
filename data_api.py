"""Fetch sample students from JSONPlaceholder without external dependencies."""

from __future__ import annotations

import json
import urllib.request

from core import Student

API_URL = "https://jsonplaceholder.typicode.com/users"

HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Vũ", "Phan", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"]
DEMT = ["Văn", "Thị", "Hữu", "Ngọc", "Thanh", "Minh", "Xuân", "Quang", "Thành", "Công", "Gia", "Bảo", "Khánh", "Phương", "Thu", "Hoài"]
TEN = ["An", "Bình", "Cường", "Dung", "Hà", "Hùng", "Khoa", "Linh", "Long", "Mai", "Nam", "Ngân", "Phong", "Quân", "Tâm", "Thảo", "Trang", "Tuấn", "Vy", "Yến"]


def _pick(pool: list[str], seed: int) -> str:
    return pool[seed % len(pool)]


def vietnamese_name(uid: int) -> str:
    return f"{_pick(HO, uid)} {_pick(DEMT, uid * 7 + 3)} {_pick(TEN, uid * 13 + 5)}"


def _score_from(n: int, salt: int) -> float:
    return round(((n * 37 + salt * 11) % 21) / 2.0, 1)


def fetch_students(limit: int = 10, timeout: int = 8) -> list[Student]:
    with urllib.request.urlopen(API_URL, timeout=timeout) as resp:
        users = json.loads(resp.read().decode("utf-8"))[:limit]
    students: list[Student] = []
    for user in users:
        uid = int(user.get("id", 0))
        students.append(Student(
            name=vietnamese_name(uid), age=15 + (uid % 5),
            math=_score_from(uid, 1), literature=_score_from(uid, 2), english=_score_from(uid, 3),
        ))
    return students


if __name__ == "__main__":
    for student in fetch_students():
        print(student.display())
