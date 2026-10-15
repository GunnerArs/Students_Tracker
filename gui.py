"""Tkinter interface for Student Tracker. Run with: python gui.py"""

from __future__ import annotations

import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from core import Repository, Student

APP_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent / "dist"
DB_FILE = str(APP_DIR / "students.db")

BG = "#1e222a"
BG_CARD = "#272c37"
BG_INPUT = "#323846"
FG = "#d7dbe4"
FG_DIM = "#8b93a3"
ACCENT = "#5b8dd6"
OK = "#56a56f"
WARN = "#d98c3f"
DANGER = "#c2564f"
BORDER = "#3a4152"
ROW_EVEN = "#242933"
ROW_ODD = "#22272f"
ROW_SEL = "#3b4b66"
RANK_COLORS = {"Giỏi": "#5bbf72", "Khá": "#5b9bd6", "Trung bình": "#d9b04f", "Yếu": "#d6605b"}
FONT = ("Ubuntu", 11)
FONT_BOLD = ("Ubuntu", 11, "bold")
FONT_TITLE = ("Ubuntu", 16, "bold")
FONT_SUB = ("Ubuntu", 10)


def _apply_style(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(".", background=BG, foreground=FG, font=FONT, bordercolor=BORDER)
    style.configure("TFrame", background=BG)
    style.configure("TEntry", fieldbackground=BG_INPUT, foreground=FG, insertcolor=FG,
                    bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER, padding=6)
    style.map("TEntry", bordercolor=[("focus", ACCENT)], lightcolor=[("focus", ACCENT)])
    style.configure("Treeview", background=BG_CARD, fieldbackground=BG_CARD, foreground=FG,
                    rowheight=34, bordercolor=BORDER, font=FONT)
    style.configure("Treeview.Heading", background=BG, foreground=FG_DIM, font=FONT_BOLD,
                    relief="flat", bordercolor=BORDER)
    style.map("Treeview", background=[("selected", ROW_SEL)], foreground=[("selected", "#ffffff")])
    style.configure("TScrollbar", background=BG_INPUT, troughcolor=BG_CARD, arrowcolor=FG)


class StudentApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Student Tracker")
        self.geometry("860x560")
        self.minsize(720, 480)
        self.configure(bg=BG)
        _apply_style(self)
        self.repo = Repository(DB_FILE)
        self.selected_id: int | None = None
        self._loading = False
        self._build_header()
        self._build_form()
        self._build_toolbar()
        self._build_list()
        self.refresh()

    def _build_header(self) -> None:
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=18, pady=(16, 6))
        tk.Label(bar, text="Student Tracker", bg=BG, fg=FG, font=FONT_TITLE).pack(side="left")
        self.count_var = tk.StringVar(value="0 học sinh")
        tk.Label(bar, textvariable=self.count_var, bg=BG, fg=FG_DIM,
                 font=FONT_SUB).pack(side="right", pady=(8, 0))

    def _build_form(self) -> None:
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="x", padx=18, pady=(8, 4))
        card = tk.Frame(outer, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x")
        pad = tk.Frame(card, bg=BG_CARD)
        pad.pack(fill="x", padx=14, pady=12)
        self.entries: dict[str, ttk.Entry] = {}
        for col, (key, label) in enumerate((
            ("name", "Tên"), ("age", "Tuổi"), ("math", "Toán"),
            ("literature", "Văn"), ("english", "Anh"),
        )):
            tk.Label(pad, text=label, bg=BG_CARD, fg=FG_DIM, font=FONT_SUB).grid(
                row=0, column=col, sticky="w", padx=(0, 16), pady=(0, 3))
            entry = ttk.Entry(pad, width=13)
            entry.grid(row=1, column=col, sticky="w", padx=(0, 16))
            self.entries[key] = entry
        btns = tk.Frame(card, bg=BG_CARD)
        btns.pack(fill="x", padx=14, pady=(0, 14))
        for label, command, color in (
            ("+  Thêm", self.add_student, OK), ("✎  Sửa", self.update_student, WARN),
            ("✕  Xóa", self.delete_student, DANGER), ("Nhập lại", self.clear_form, BG_INPUT),
        ):
            tk.Button(btns, text=label, command=command, bg=color, fg="#ffffff",
                      activebackground=BORDER, relief="flat", font=FONT_BOLD,
                      cursor="hand2", padx=14, pady=6).pack(side="left", padx=(0, 6))

    def _build_toolbar(self) -> None:
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=18, pady=(6, 6))
        self.api_btn = tk.Button(bar, text="⇩  Tải mẫu từ API", command=self.load_from_api,
                                 bg=ACCENT, fg="#ffffff", activebackground=BG_INPUT,
                                 relief="flat", font=FONT_BOLD, cursor="hand2", padx=14, pady=6)
        self.api_btn.pack(side="left")
        self.status = tk.Label(bar, text="", bg=BG, fg=FG_DIM, font=FONT_SUB)
        self.status.pack(side="left", padx=12)
        search_wrap = tk.Frame(bar, bg=BG_INPUT, highlightbackground=BORDER, highlightthickness=1)
        search_wrap.pack(side="right")
        tk.Label(search_wrap, text="🔍", bg=BG_INPUT, fg=FG_DIM, font=FONT).pack(side="left", padx=(8, 2), pady=4)
        self.search_entry = tk.Entry(search_wrap, bg=BG_INPUT, fg=FG, insertbackground=FG,
                                     relief="flat", font=FONT, width=22)
        self.search_entry.pack(side="left", padx=(0, 8), pady=5, ipady=3)
        self.search_entry.bind("<KeyRelease>", lambda _event: self.refresh())

    def _build_list(self) -> None:
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True, padx=18, pady=(2, 14))
        card = tk.Frame(wrap, bg=BG_CARD, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True)
        columns = ("id", "name", "age", "avg", "ranking")
        headers = {"id": "  ID", "name": "Họ tên", "age": "Tuổi", "avg": "ĐTB", "ranking": "Xếp loại"}
        widths = {"id": 55, "name": 280, "age": 70, "avg": 90, "ranking": 150}
        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=11)
        for col in columns:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=widths[col], anchor="center" if col in ("id", "age", "avg") else "w",
                             stretch=(col == "name"))
        sb = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)
        sb.pack(side="right", fill="y", pady=4)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        for rank, color in RANK_COLORS.items():
            self.tree.tag_configure(f"rank_{rank}", foreground=color)
        self.tree.tag_configure("even", background=ROW_EVEN)
        self.tree.tag_configure("odd", background=ROW_ODD)

    def read_form(self) -> Student | None:
        try:
            name = self.entries["name"].get().strip()
            if not name:
                raise ValueError("Tên")
            student = Student(
                name=name, age=int(self.entries["age"].get()),
                math=float(self.entries["math"].get().replace(",", ".")),
                literature=float(self.entries["literature"].get().replace(",", ".")),
                english=float(self.entries["english"].get().replace(",", ".")),
            )
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ và đúng định dạng (tuổi nguyên, điểm 0-10).")
            return None
        if not all(0 <= score <= 10 for score in (student.math, student.literature, student.english)):
            messagebox.showerror("Lỗi", "Điểm phải trong khoảng 0 đến 10.")
            return None
        if student.age <= 0:
            messagebox.showerror("Lỗi", "Tuổi phải lớn hơn 0.")
            return None
        return student

    def clear_form(self) -> None:
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.selected_id = None

    def add_student(self) -> None:
        student = self.read_form()
        if student:
            self.repo.add(student)
            self.clear_form()
            self.refresh()

    def update_student(self) -> None:
        if self.selected_id is None:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng trong danh sách trước khi sửa.")
            return
        student = self.read_form()
        if student:
            student.student_id = self.selected_id
            self.repo.update(student)
            self.clear_form()
            self.refresh()

    def delete_student(self) -> None:
        if self.selected_id is None:
            messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng trong danh sách trước khi xóa.")
            return
        if messagebox.askyesno("Xác nhận", f"Xóa học sinh id={self.selected_id}?"):
            self.repo.delete(self.selected_id)
            self.clear_form()
            self.refresh()

    def on_select(self, _event) -> None:
        selected = self.tree.selection()
        if selected:
            self.selected_id = int(self.tree.item(selected[0], "values")[0])

    def refresh(self) -> None:
        self.tree.delete(*self.tree.get_children())
        keyword = self.search_entry.get().strip().lower()
        shown = 0
        for index, student in enumerate(self.repo.list_all()):
            if keyword and keyword not in student.name.lower():
                continue
            self.tree.insert("", "end", values=(student.student_id, student.name, student.age,
                             f"{student.average:.2f}", student.ranking),
                             tags=(f"rank_{student.ranking}", "even" if index % 2 == 0 else "odd"))
            shown += 1
        self.count_var.set(f"{shown} học sinh")

    def load_from_api(self) -> None:
        if self._loading:
            return
        self._loading = True
        self.api_btn.config(state="disabled")
        self.status.config(text="Đang tải từ API...")

        def worker() -> None:
            try:
                from data_api import fetch_students
                students = fetch_students(limit=10)
                self.after(0, lambda: self._on_api_done(students, None))
            except Exception as exc:
                self.after(0, lambda error=exc: self._on_api_done([], error))

        threading.Thread(target=worker, daemon=True).start()

    def _on_api_done(self, students: list[Student], error: Exception | None) -> None:
        if error is not None:
            self.status.config(text=f"Lỗi API: {error}")
            messagebox.showerror("Lỗi", f"Không tải được từ API:\n{error}")
        else:
            added = self.repo.add_missing(students)
            self.refresh()
            self.status.config(text=f"Đã thêm {added} học sinh; bỏ qua {len(students) - added} bản ghi đã có.")
        self._loading = False
        self.api_btn.config(state="normal")

    def destroy(self) -> None:
        self.repo.close()
        super().destroy()


if __name__ == "__main__":
    StudentApp().mainloop()
