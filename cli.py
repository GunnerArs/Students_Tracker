"""Command line interface for Student Tracker."""

from __future__ import annotations

from pathlib import Path

from core import Repository, Student

MENU = """
===== STUDENT TRACKER =====
1. Thêm học sinh
2. Hiển thị danh sách
3. Tìm theo tên
4. Sửa thông tin
5. Xóa học sinh
6. Thoát
=========================="""


def nhap_diem(prompt: str) -> float:
    while True:
        try:
            val = float(input(prompt).strip().replace(",", "."))
        except ValueError:
            print("  ! Vui lòng nhập số hợp lệ.")
            continue
        if 0 <= val <= 10:
            return val
        print("  ! Điểm phải trong khoảng 0 đến 10.")


def nhap_tuoi(prompt: str) -> int:
    while True:
        try:
            val = int(input(prompt).strip())
        except ValueError:
            print("  ! Vui lòng nhập số nguyên hợp lệ.")
            continue
        if val > 0:
            return val
        print("  ! Tuổi phải lớn hơn 0.")


def hoc_sinh_tu_input() -> Student:
    name = input("  Tên: ").strip()
    while not name:
        name = input("  Tên không được trống, nhập lại: ").strip()
    age = nhap_tuoi("  Tuổi: ")
    print("  Nhập điểm 3 môn (0-10):")
    math = nhap_diem("    Toán: ")
    literature = nhap_diem("    Văn:  ")
    english = nhap_diem("    Anh:  ")
    return Student(name, age, math, literature, english)


def action_add(repo: Repository) -> None:
    print("\n-- Thêm học sinh --")
    student = hoc_sinh_tu_input()
    repo.add(student)
    print(f"  Đã lưu: {student.display()}")


def action_show(repo: Repository) -> None:
    print("\n-- Danh sách học sinh --")
    students = repo.list_all()
    if not students:
        print("  Danh sách trống.")
        return
    for student in students:
        print("  " + student.display())
    print(f"  Tổng số: {len(students)} học sinh.")


def action_search(repo: Repository) -> None:
    print("\n-- Tìm kiếm theo tên --")
    keyword = input("  Nhập tên cần tìm: ").strip()
    found = False
    for student in repo.list_all():
        if keyword.lower() in student.name.lower():
            print("  " + student.display())
            found = True
    if not found:
        print("  Không tìm thấy.")


def action_edit(repo: Repository) -> None:
    print("\n-- Sửa thông tin --")
    try:
        sid = int(input("  Nhập id học sinh cần sửa: ").strip())
    except ValueError:
        print("  ! id không hợp lệ.")
        return
    student = repo.get(sid)
    if student is None:
        print("  Không tìm thấy.")
        return
    print(f"  Hiện tại: {student.display()}")
    new = hoc_sinh_tu_input()
    new.student_id = sid
    repo.update(new)
    print(f"  Đã sửa: {new.display()}")


def action_delete(repo: Repository) -> None:
    print("\n-- Xóa học sinh --")
    try:
        sid = int(input("  Nhập id học sinh cần xóa: ").strip())
    except ValueError:
        print("  ! id không hợp lệ.")
        return
    if repo.delete(sid):
        print(f"  Đã xóa học sinh id={sid}.")
    else:
        print("  Không tìm thấy.")


def main() -> None:
    repo = Repository(str(Path(__file__).resolve().parent / "dist" / "students.db"))
    try:
        while True:
            print(MENU)
            choice = input("Chọn chức năng (1-6): ").strip()
            if choice == "1":
                action_add(repo)
            elif choice == "2":
                action_show(repo)
            elif choice == "3":
                action_search(repo)
            elif choice == "4":
                action_edit(repo)
            elif choice == "5":
                action_delete(repo)
            elif choice == "6":
                print("Tạm biệt!")
                break
            else:
                print("  ! Lựa chọn không hợp lệ, vui lòng chọn 1-6.")
    finally:
        repo.close()


if __name__ == "__main__":
    main()
