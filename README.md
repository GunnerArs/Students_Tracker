# Student Tracker

Ứng dụng quản lý học sinh dành cho giáo viên: nhập tên, tuổi và điểm Toán, Văn, Anh; tính điểm trung bình, xếp loại học lực và tìm kiếm theo tên. Dự án được xây dựng theo [yêu cầu bài kiểm tra](yeucau.md), với cả giao diện dòng lệnh (CLI) và giao diện cửa sổ (Tkinter).

## Tính năng đã xây dựng

- Thêm, xem, sửa và xóa học sinh. Mỗi học sinh có ID, tên, tuổi và điểm ba môn. ID được đánh lại liên tiếp từ 1 sau khi xóa; file CSV cũ có ID bị khuyết được cập nhật khi mở ứng dụng.
- Tính **ĐTB = (Toán + Văn + Anh) / 3**, hiển thị đến hai chữ số thập phân và xếp loại:

  | Điểm trung bình | Xếp loại |
  | --- | --- |
  | Từ 8,0 trở lên | Giỏi |
  | Từ 6,5 đến dưới 8,0 | Khá |
  | Từ 5,0 đến dưới 6,5 | Trung bình |
  | Dưới 5,0 | Yếu |

- Tìm học sinh theo một phần tên, không phân biệt chữ hoa và chữ thường. CLI thông báo khi không tìm thấy; GUI hiển thị danh sách đã lọc.
- CLI có menu sáu lựa chọn: thêm, xem, tìm, sửa, xóa và thoát.
- GUI Tkinter có form nhập, nút thao tác và bảng `Treeview`. Tên không được để trống, tuổi phải là số nguyên dương và điểm phải từ 0 đến 10.
- Nút **Tải mẫu từ API** trong GUI lấy tối đa 10 mục từ JSONPlaceholder, tạo tên tiếng Việt và điểm mẫu theo ID rồi thêm vào danh sách. Những bản ghi có cùng tên, tuổi và ba điểm đã tồn tại trong CSV sẽ được bỏ qua, nên tải lại không tạo thêm bản sao. Giao diện cho biết số bản ghi đã thêm và đã bỏ qua. Việc tải chạy trên luồng nền để giao diện tiếp tục phản hồi. Tính năng này cần Internet.
- Dữ liệu được lưu trong `dist/students.csv` và vẫn còn khi mở lại ứng dụng. Mã nguồn tách thành các lớp `Student`, `StudentManager` và `Repository`.
- Có bản chạy Windows 64-bit được đóng gói bằng PyInstaller.

Ứng dụng hiện thêm từng học sinh qua form hoặc menu; chưa có bước nhập trước số lượng **N**. Theo thay đổi của dự án, dữ liệu được lưu bằng **CSV thay cho SQLite** nêu trong yêu cầu gốc.

## Chạy ứng dụng

### Bản Windows đã đóng gói

Mở `dist/student_tracker.exe`. Máy đích cần Windows 64-bit, không cần cài Python. Đặt `students.csv` cùng thư mục với `.exe` để mang theo dữ liệu hiện có. Nếu thiếu file CSV, ứng dụng sẽ tạo một file mới với danh sách trống. Thư mục chứa hai file cần cho phép ứng dụng ghi dữ liệu.

### Chạy từ mã nguồn

Cần Python 3.10 trở lên với Tkinter để chạy GUI. Từ thư mục `student_tracker`:

```powershell
python gui.py
```

Hoặc chạy bản dòng lệnh:

```powershell
python cli.py
```

Cả hai bản dùng chung `dist/students.csv`; dữ liệu nhập ở một bản sẽ xuất hiện khi mở bản kia. Các thư viện dùng khi chạy mã nguồn đều thuộc thư viện chuẩn Python.

### Đóng gói lại trên Windows

Cài PyInstaller rồi chạy từ thư mục `student_tracker`:

```powershell
python -m pip install pyinstaller
python -m PyInstaller --clean --noconfirm --distpath dist student_tracker.spec
```

File mới nằm tại `dist/student_tracker.exe`. CSV không được nhúng vào `.exe`; giữ `dist/students.csv` riêng để bảo toàn dữ liệu khi đóng gói lại hoặc chia sẻ cho máy khác.

Khi đưa mã nguồn lên GitHub, `dist/students.csv` được bỏ qua để tránh công khai tên và điểm của học sinh. Người tải dự án có thể chạy ứng dụng để tạo CSV trống, hoặc tự đặt file CSV của mình cạnh `.exe`.

## Cấu trúc dự án

```text
student_tracker/
    ├── yeucau.md             # Yêu cầu bài kiểm tra
    ├── .gitignore            # Bỏ qua dữ liệu cá nhân và file build tạm
    ├── README.md              # Hướng dẫn
    ├── cli.py                 # Giao diện dòng lệnh
    ├── gui.py                 # Giao diện Tkinter
    ├── core.py                # Tính năng
    ├── data_api.py            # Lấy dữ liệu mẫu từ API
    ├── student_tracker.spec   # Cấu hình PyInstaller
    └── dist/
        ├── student_tracker.exe
        └── students.csv
```

CSV có các cột `id,name,age,math,literature,english`, mã hóa UTF-8. Điểm trung bình và xếp loại được tính từ ba điểm môn học khi hiển thị, không lưu thành cột riêng. Có thể sao lưu dữ liệu bằng cách copy `students.csv` khi ứng dụng đã đóng.
