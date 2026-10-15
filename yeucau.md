# YÊU CẦU BÀI KIỂM TRA – DỰ ÁN PYTHON

## Student Tracker – Quản lý học sinh & xếp loại

### 1. Bối cảnh sản phẩm

Trung tâm cần một công cụ nhỏ để giáo viên nhập thông tin học sinh trong lớp và nhanh chóng:

- Lưu danh sách học sinh theo buổi học.
- Tính điểm trung bình và xếp loại học lực.
- Tìm kiếm học sinh theo tên để xem thông tin.

**Nhiệm vụ:** Xây dựng một chương trình Python đáp ứng các nhu cầu trên.

---

## 2. Các tính năng sản phẩm cần có

### A. Tính năng bắt buộc (Core)

*Mục tiêu: kiểm tra khả năng xây dựng sản phẩm với kiến thức Python cơ bản.*

#### 1. Nhập danh sách học sinh

- Người dùng nhập số lượng học sinh **N**.
- Với mỗi học sinh, nhập tối thiểu:
  - Tên.
  - Tuổi (hoặc lớp).
  - Điểm 3 môn: **Toán – Văn – Anh** (có thể đổi tên môn, nhưng phải có ít nhất 3 số điểm).

#### 2. Tính điểm trung bình

- Công thức: **ĐTB = (điểm 1 + điểm 2 + điểm 3) / 3**.
- In hoặc hiển thị điểm trung bình của từng học sinh.

#### 3. Xếp loại học lực bằng điều kiện

| Điểm trung bình | Xếp loại |
|---|---|
| ĐTB ≥ 8.0 | Giỏi |
| 6.5 ≤ ĐTB < 8.0 | Khá |
| 5.0 ≤ ĐTB < 6.5 | Trung bình |
| ĐTB < 5.0 | Yếu |

#### 4. Hiển thị danh sách tổng hợp

Hiển thị mỗi học sinh với các thông tin:

- Tên.
- Tuổi hoặc lớp.
- Điểm trung bình.
- Xếp loại.

#### 5. Tìm kiếm học sinh theo tên

- Người dùng nhập tên cần tìm.
- Nếu tìm thấy: hiển thị đầy đủ thông tin học sinh.
- Nếu không tìm thấy: thông báo **“Không tìm thấy”**.
- Khuyến khích sử dụng biến cờ hoặc logic tìm kiếm rõ ràng.

#### 6. Tổ chức chương trình bằng hàm

Các kiến thức Python tối thiểu **bắt buộc thể hiện trong mã nguồn (HP5)**:

- Biến, kiểu dữ liệu, toán tử.
- `input()`.
- `if/elif/else`.
- `for` (**bắt buộc**).
- `while` (khuyến khích, không bắt buộc trong phần Core).
- List (**bắt buộc**).
- Function (**bắt buộc**).

---

### B. Tính năng nâng cao (Optional – cộng điểm/sàng lọc)

Ứng viên có thể chọn thực hiện một phần hoặc toàn bộ. Làm được nhiều tính năng nâng cao có thể được đánh giá cao hơn.

#### Nâng cao 1: Menu thao tác bằng vòng lặp

Chương trình chạy theo menu:

1. Thêm học sinh.
2. Hiển thị danh sách.
3. Tìm theo tên.
4. Sửa thông tin.
5. Xóa học sinh.
6. Thoát.

#### Nâng cao 2: Giao diện Tkinter (GUI)

- Có form nhập bằng `Entry`.
- Có nút thao tác bằng `Button`.
- Có danh sách hiển thị bằng `Listbox` hoặc `Treeview`.
- Người dùng thao tác bằng chuột thay vì nhập trong terminal.

#### Nâng cao 3 (HP6): Lưu dữ liệu bằng SQLite

- Lưu danh sách học sinh vào cơ sở dữ liệu.
- Hỗ trợ CRUD: thêm, hiển thị, sửa, xóa.
- Khi mở lại chương trình, dữ liệu vẫn còn.

#### Nâng cao 4 (HP7): Tổ chức code theo OOP

- Sử dụng các lớp, ví dụ: `Student`, `StudentManager`, `Repository`.
- Tách riêng logic dữ liệu và xử lý.

#### Nâng cao 5: Tích hợp API / Threading / Đóng gói

- **API:** Lấy danh sách câu hỏi hoặc dữ liệu mẫu và nhập vào chương trình.
- **Threading:** Tải dữ liệu mà không làm đơ giao diện (nếu có GUI).
- **Đóng gói:** Sử dụng PyInstaller để tạo file chạy.

---

## 3. Hình thức nộp sản phẩm

Theo thông tin biểu mẫu ứng tuyển:

- **Nếu sản phẩm có thể chia sẻ bằng đường link:** Dán trực tiếp link sản phẩm.
- **Nếu sản phẩm không có link chia sẻ trực tiếp:** Tải sản phẩm lên Google Drive và cung cấp link Drive.

