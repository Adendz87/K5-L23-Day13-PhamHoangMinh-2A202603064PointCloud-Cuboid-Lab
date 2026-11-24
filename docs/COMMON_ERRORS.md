# Lỗi hay gặp và cách tự gỡ

Đọc đúng dòng báo lỗi trên màn hình rồi tìm trong bảng. Không thấy thì hỏi bạn bên cạnh, sau đó hỏi coach.

## 1. Terminal và Python

| Triệu chứng | Nguyên nhân | Cách gỡ |
|---|---|---|
| Windows: `python` mở Microsoft Store hoặc không in gì | Chưa cài Python thật | Cài theo [SETUP.md](SETUP.md) mục 2, mở lại PowerShell |
| macOS: `command not found: python` | Chưa kích hoạt `.venv` | `source .venv/bin/activate`. Ngoài `.venv` thì dùng `python3` |
| Windows: `Activate.ps1 cannot be loaded because running scripts is disabled` | Chính sách PowerShell chặn script | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, rồi kích hoạt lại |
| Windows: `source : The term 'source' is not recognized` | Gõ lệnh macOS trên PowerShell | Dùng `.\.venv\Scripts\Activate.ps1` |
| macOS: `zsh: no such file or directory: .\.venv\Scripts\Activate.ps1` | Gõ lệnh Windows trên macOS | Dùng `source .venv/bin/activate` |
| `can't open file '...scripts/lab.py': No such file or directory` | Đang đứng sai thư mục | `cd` vào thư mục gốc repo (thư mục có `README.md`) |
| `Thiếu cvat-sdk. Chạy: pip install -r requirements.txt` hoặc `Thiếu Pillow` | Chưa cài thư viện, hoặc chưa kích hoạt `.venv` | Kích hoạt `.venv`, rồi `python -m pip install -r requirements.txt` |
| `pip install` rất chậm hoặc lỗi mạng | Mạng lớp yếu | Thử lại, đổi mạng, hoặc ghép với bạn bên cạnh |
| `Chưa điền student trong configs/lab.ini` hoặc `Chưa điền cvat_user` | Chưa điền cấu hình | Mở `configs/lab.ini`, điền mã số và tên đăng nhập CVAT, lưu lại |
| `The '<' operator is reserved for future use` (Windows) hoặc `no such file or directory: MSHV` (macOS) | Chưa thay chỗ `<...>` trong lệnh | Thay `<MSHV>`, `<tài-khoản>` bằng giá trị thật, bỏ dấu `<` `>` |
| `SyntaxError` ngay khi chạy, có `list[dict]` hoặc `str | None` | Python cũ hơn 3.10 | Cài Python 3.10+ và tạo lại `.venv` |
| Chữ tiếng Việt thành ký tự lạ trên PowerShell | Bảng mã của cửa sổ | Chạy `chcp 65001` rồi chạy lại lệnh. Nội dung file kết quả không bị ảnh hưởng |

## 2. Dữ liệu

| Triệu chứng | Nguyên nhân | Cách gỡ |
|---|---|---|
| `Không thấy sequence_XX/lidar/*.bin trong ...` | `data` trong `configs/lab.ini` trỏ sai thư mục, hoặc giải nén lồng hai lớp (`data-VF/Data-VF/sequence_01`) | `data` phải trỏ vào thư mục **chứa trực tiếp** `sequence_01 … sequence_05` |
| Frame in ra `camera=0` hoặc nhỏ hơn 7 | Giải nén thiếu thư mục `cameras`, hoặc zip tải chưa xong | Kiểm kích thước zip (khoảng 600 MB), giải nén lại |
| `Mã số không hợp lệ` | Mã có dấu cách, dấu tiếng Việt hoặc ký tự lạ | Chỉ dùng chữ không dấu, số, `-`, `_`; dài 2–32 ký tự |
| Hướng xe trên view Top ngược với mô tả (phía trước là +y) | Đang dùng bản `data-VF` cũ | Tải lại bản mới theo link trong [../data/README.md](../data/README.md), xóa bản cũ |

## 3. Kết nối CVAT và tạo task

| Triệu chứng | Nguyên nhân | Cách gỡ |
|---|---|---|
| `Connection refused`, `Max retries exceeded`, không nối được máy chủ | CVAT chưa chạy, sai địa chỉ, hoặc ngoài mạng lớp | Mở địa chỉ bằng trình duyệt trước. CVAT local: `docker compose up -d` trong thư mục `cvat`, chờ 1 phút |
| Đăng nhập thất bại (401, `Unable to log in`) | Sai tên đăng nhập hoặc mật khẩu | Thử đăng nhập bằng trình duyệt. Tên đăng nhập là username, không phải email |
| `Đã có task D13-…` | Bạn đã tạo task rồi | Mở task cũ theo đường dẫn lệnh in ra. **Không** thêm `--replace` nếu đã vẽ gì |
| Lệnh tạo task chạy vài phút chưa xong | Cả lớp tải lên cùng lúc, hoặc máy yếu | Chờ. Đừng chạy lại nhiều lần |
| `Không thấy task D13-…` khi chạy `report` | `cvat_host`, `cvat_user` hoặc `cvat_org` trong `configs/lab.ini` đã đổi so với lúc tạo task | Trả `configs/lab.ini` về đúng giá trị đã dùng khi tạo task |
| Trang CVAT trắng hoặc 502 | Server chưa khởi động xong | Chờ 1–2 phút, `docker compose ps` |

## 4. Trong CVAT 3D

| Triệu chứng | Nguyên nhân | Cách gỡ |
|---|---|---|
| Không thấy ảnh camera | Ảnh chưa tải, hoặc khung ảnh liên quan đang đóng | Mở khung ảnh liên quan (context image) của job, chờ tải. Vẫn không có thì báo coach |
| Point cloud không hiện, màn hình đen | Trình duyệt không phải Chrome/Edge, hoặc WebGL tắt | Dùng Chrome hoặc Edge, bật tăng tốc phần cứng |
| Xoay, phóng to rất giật | Máy yếu, nhiều tab | Đóng tab và ứng dụng khác; máy 8 GB làm theo [CVAT_SETUP.md](CVAT_SETUP.md) mục 6 |
| Cuboid xong nhưng mũi tên ngược đầu xe | Quay nhầm 180° | Xoay yaw 180°, kiểm lại với ảnh camera |
| Không thấy mũi tên đỏ | Chưa bật orientation | Tích ô **orientation** trong phần Appearance |
| Đáy cuboid lơ lửng hoặc chìm | Chỉ chỉnh ở view Top | Chỉnh ở Side và Front; xem lại `z_bottom` ở bảng A |
| Vẽ ra Track thay vì Shape | Bấm nhầm nút Track | Xóa và vẽ lại bằng **Shape**. Hôm nay không dùng track |
| Tìm không ra biểu tượng vàng chiếu box lên ảnh | Bản CVAT này có thể không có tính năng đó | Dùng `python scripts/lab.py preview` để xem cuboid trên ảnh camera |
| Tưởng "phía trước là +x" hoặc "y là bên trái" | Nhớ hệ tọa độ khác (KITTI, ROS) | Xem cam01: ảnh trước trùng hướng −y. x dương là trái, y dương là sau |
| Mất cuboid sau khi đóng tab | Chưa Save | Save sau mỗi frame (`Ctrl+S`, macOS `Cmd+S`) |

## 5. Bảng A và tự kiểm

| Triệu chứng | Nguyên nhân | Cách gỡ |
|---|---|---|
| `Bảng A trống` hoặc thiếu cuboid | Chưa Save trong CVAT | Save rồi chạy lại `report` |
| `preview` / `selfcheck` báo không thấy file bảng A | Chưa chạy `report` | Chạy `python scripts/lab.py report` trước, hoặc chạy `sync` |
| `length` và `width` đổi chỗ ở **mọi** xe dù mũi tên đỏ dọc thân xe | Thứ tự trục của CVAT khác với công cụ | Báo coach. Không vẽ lại |
| Excel mở CSV ra chữ lạ hoặc dồn một cột | Excel đoán sai bảng mã hoặc dấu phân cách | Data → From Text/CSV, chọn **65001: Unicode (UTF-8)**, phân cách dấu phẩy. Hoặc mở bằng Google Sheets, Numbers |
| Excel hiện `-1.7` thành ngày tháng hoặc số sai | Vùng miền dùng dấu phẩy thập phân | Nhập qua From Text/CSV như trên; **không lưu đè** file CSV gốc |
| `check_submission.py` báo bảng A có cột khác bản do `report` sinh ra | Đã lưu đè CSV từ Excel hoặc sửa tay | Chạy lại `python scripts/lab.py sync` để sinh lại |
| `check_submission.py` báo phiếu tự kiểm không khớp bảng A | Chạy `report` sau `selfcheck` | Chạy `python scripts/lab.py sync` |
| `check_submission.py` báo repo đang theo dõi file dữ liệu/ảnh | Đã `git add -f` ảnh hoặc dữ liệu | `git rm --cached <file>`, commit lại. Nếu đã push, báo coach ngay |
| `selfcheck` cờ gần hết người đi bộ | Ngưỡng của công cụ chặt với vật nhỏ | Xem lại từng hộp; hộp đúng thì giữ và ghi một dòng lý do vào báo cáo |
