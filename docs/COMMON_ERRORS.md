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
| `pip install` rất chậm hoặc lỗi mạng | Mạng chậm | Thử lại, đổi mạng, hoặc ghép với bạn bên cạnh. Cài **trước** buổi học |
| `Chưa điền student trong configs/lab.ini` hoặc `Chưa điền cvat_user` | Chưa điền cấu hình | Mở `configs/lab.ini`, điền mã số và tên đăng nhập CVAT, lưu lại |
| `Không đọc được ...configs\lab.ini` | File bị lưu sai bảng mã, hoặc mất dòng `[lab]` | Mở bằng Notepad (macOS: TextEdit), giữ dòng `[lab]`, mỗi khoá một dòng `tên = giá trị`; Notepad chọn **Save as → Encoding: UTF-8** |
| `The '<' operator is reserved for future use` (Windows) hoặc `no such file or directory: MSHV` (macOS) | Chưa thay chỗ `<...>` trong lệnh | Thay `<MSHV>`, `<tài-khoản>` bằng giá trị thật, bỏ dấu `<` `>` |
| `pip install` báo `requires a different python version`, `No matching distribution found for cvat-sdk` hoặc `ResolutionImpossible`; hoặc `scripts/lab.py` in `CẢNH BÁO: đang chạy Python 3.…` | `.venv` được tạo bằng Python cũ hơn 3.11 (macOS có sẵn Python 3.9) | Cài Python 3.12 ([SETUP.md](SETUP.md) mục 2). Chạy `deactivate`, xoá thư mục `.venv` (Windows: `Remove-Item -Recurse -Force .venv`; macOS: `rm -rf .venv`), tạo lại bằng `py -3.12 -m venv .venv` (Windows) hoặc `python3.12 -m venv .venv` (macOS), kích hoạt rồi cài lại thư viện. **Đừng** sửa dòng `cvat-sdk` trong `requirements.txt` |
| Windows: chữ tiếng Việt thành ký tự lạ, hoặc `UnicodeEncodeError` khi dùng `>` hay `\|` | Bảng mã của PowerShell khi chuyển kết quả ra file hoặc lệnh khác | Chạy lệnh không chuyển hướng (in thẳng ra màn hình). Cần ghi ra file thì chạy `[Console]::OutputEncoding = [Text.Encoding]::UTF8` trước; xem file bằng Notepad. Nội dung các file CSV không bị ảnh hưởng |

## 2. Dữ liệu

| Triệu chứng | Nguyên nhân | Cách gỡ |
|---|---|---|
| Giải nén báo `Incorrect passphrase` hoặc `Couldn't read passphrase` | Gõ sai mật khẩu zip, hoặc chạy `tar` ở nơi không có ô nhập | Xoá phần đã giải nén, chạy lại `tar -xf` trong PowerShell/Terminal và gõ đúng mật khẩu GV gửi ([SETUP.md](SETUP.md) mục 4) |
| `unzip` (macOS) báo `need PK compat. v5.1` hoặc `unsupported compression method 99`; `Expand-Archive` (Windows) báo lỗi | Zip mã hoá kiểu AES | Dùng `tar -xf` như [SETUP.md](SETUP.md) mục 4, hoặc 7-Zip (Windows) / Keka (macOS) |
| `calib.json thiếu hoặc hỏng` hoặc `... toàn số 0` | Giải nén dở hoặc sai mật khẩu, file ra rỗng | Xoá thư mục dữ liệu, giải nén lại |
| `CẢNH BÁO: data-VF thiếu file` | Zip tải chưa xong, hoặc giải nén dở | Kiểm kích thước zip (khoảng 600 MB), tải lại nếu cần, giải nén lại |
| `Không thấy sequence_XX/lidar/*.bin trong ...` | `data` trong `configs/lab.ini` trỏ sai thư mục, hoặc giải nén lồng hai lớp (`data-VF/Data-VF/sequence_01`) | `data` phải trỏ vào thư mục **chứa trực tiếp** `sequence_01 … sequence_05`; không cần ngoặc kép |
| Frame in ra `camera=0` hoặc nhỏ hơn 7 | Giải nén thiếu thư mục `cameras` | Giải nén lại |
| `Mã số không hợp lệ` | Mã có dấu cách, dấu tiếng Việt hoặc ký tự lạ | Chỉ dùng chữ không dấu, số, `-`, `_`; dài 2–32 ký tự |
| `lab.py` báo `data-VF này là bản cũ` | Đang dùng `data-VF` trước bản cập nhật 22/11/2026 (hệ trục cũ: phía trước là +x) | Tải lại bản cập nhật theo link GV gửi riêng, xoá bản cũ. Task đã tạo bằng bản cũ thì tạo lại bằng `python scripts/lab.py task --replace` (mất cuboid đã vẽ) |
| Không có báo lỗi, nhưng xe phía trước nằm ở +x, xe cùng chiều phía trước ra `yaw_deg` gần 0° hoặc 360°, `az_deg` của vật phía trước gần +90° | Dấu hiệu dữ liệu hệ trục cũ (lẫn bản cũ và bản mới) | Như dòng trên; báo coach |

## 3. Kết nối CVAT và tạo task

| Triệu chứng | Nguyên nhân | Cách gỡ |
|---|---|---|
| `Không nối được CVAT ở http://localhost:8080` | CVAT chưa chạy hoặc sai địa chỉ | Mở địa chỉ bằng trình duyệt trước. Chạy `docker compose up -d` trong thư mục `cvat` **của CVAT** (cạnh repo, không phải thư mục `cvat/` trong repo), chờ 1 phút |
| `CVAT từ chối đăng nhập` | Sai tên đăng nhập hoặc mật khẩu | Thử đăng nhập bằng trình duyệt. Tên đăng nhập là username, không phải email |
| `cvat_host ... phải có dạng http://localhost:8080` | Dòng `cvat_host` trong `configs/lab.ini` bị sửa sai | Ghi lại `cvat_host = http://localhost:8080` |
| `Server version … is not compatible with SDK version …` | CVAT trên máy là 2.82 (từ Ngày 12), `cvat-sdk` là 2.83 | Chỉ là cảnh báo: bỏ qua, đừng cài lại `cvat-sdk`. Kiểm bằng `python -m pip show cvat-sdk` nếu cần ([CVAT_SETUP.md](CVAT_SETUP.md) mục 8) |
| `Đã có task D13-…` | Bạn đã tạo task rồi | Mở task cũ theo đường dẫn lệnh in ra. **Không** thêm `--replace` nếu đã vẽ gì |
| Lệnh tạo task chạy vài phút chưa xong | Máy yếu, hoặc Docker còn đang khởi động | Chờ. Đừng chạy lại nhiều lần |
| Lệnh `task` lỗi mà trình duyệt vẫn mở được CVAT | Lỗi khi gửi dữ liệu qua `cvat-sdk` | Tạo task bằng tay ([CVAT_SETUP.md](CVAT_SETUP.md) mục 7) |
| `Không thấy task D13-…` khi chạy `report` | `cvat_host`, `cvat_user` hoặc `cvat_org` trong `configs/lab.ini` đã đổi so với lúc tạo task; hoặc task tạo bằng tay bị đặt sai tên | Trả `configs/lab.ini` về đúng giá trị đã dùng khi tạo task; tên task phải đúng `D13-<MÃ SỐ>` |
| Trang CVAT trắng hoặc 502 | Server chưa khởi động xong | Chờ 1–2 phút, `docker compose ps` |

## 4. Trong CVAT 3D

| Triệu chứng | Nguyên nhân | Cách gỡ |
|---|---|---|
| Chỉ thấy 3 ảnh camera (cam01, cam03, cam05) | Bố cục mặc định chỉ hiện 3 ảnh | Rê chuột lên một khung ảnh, bấm biểu tượng bánh răng ở góc khung, chọn camera khác ([CVAT_SETUP.md](CVAT_SETUP.md) mục 9) |
| Không thấy ảnh camera nào | Ảnh chưa tải, hoặc đã đóng khung ảnh | Chờ tải; dùng nút đặt lại bố cục của khu ảnh. Vẫn không có thì báo coach |
| Khung Top, Side, Front gần như trống | Ba khung này chỉ chiếu cuboid đang chọn | Chọn một cuboid. Muốn nhìn cả cảnh từ trên xuống thì xoay khung 3D |
| Bấm vào vật mà không ra cuboid | Cuboid được đặt bằng **nháy đúp** | Bấm Shape, đưa hộp tới vật rồi nháy đúp |
| Đang vẽ thì kéo chuột không xoay được khung 3D | CVAT khoá xoay khi đang đặt hộp | Chỉnh góc nhìn trước khi bấm Shape, hoặc dùng con lăn và các nút U I O J K L, mũi tên ở góc khung 3D |
| Point cloud không hiện, màn hình đen | Trình duyệt không phải Chrome/Edge, hoặc WebGL tắt | Dùng Chrome hoặc Edge, bật tăng tốc phần cứng |
| Xoay, phóng to rất giật | Máy yếu, nhiều tab | Đóng tab và ứng dụng khác; máy 8 GB làm theo [CVAT_SETUP.md](CVAT_SETUP.md) mục 6 |
| Cuboid xong nhưng mũi tên ngược đầu xe | Quay nhầm 180° | Chọn cuboid, ở khung **Top** kéo nút xoay nửa vòng, kiểm lại với ảnh camera |
| Hộp bị nghiêng ở Side hoặc Front | Lỡ kéo nút xoay ở Side/Front | `Ctrl+Z` (macOS `Cmd+Z`). Chỉ xoay ở Top; bảng A không ghi độ nghiêng |
| Không thấy mũi tên đỏ | Chưa bật hiển thị hướng | Tích ô **Cuboid orientation** trong phần Appearance |
| Đáy cuboid lơ lửng hoặc chìm | Mới chỉnh ở Top | Chỉnh ở Side và Front; xem lại `z_bottom` ở bảng A |
| Thẻ cuboid ghi **CUBOID TRACK**, hoặc cuboid vẫn hiện ở các frame sau; `report` báo `cuboid dạng Track` | Bấm nhầm Track (hoặc bấm `N` sau một lần vẽ Track) | Track không vào bảng A, không được chấm. Chọn cuboid, bấm `Delete`, vẽ lại bằng **Shape**; thẻ phải ghi CUBOID SHAPE |
| Không tìm thấy ô "occluded" | Occluded là nút hình người trên thẻ cuboid | Bấm nút hình người (thành hình hai người là đã bật), hoặc chọn cuboid rồi bấm `Q` |
| Tìm không ra biểu tượng vàng chiếu box lên ảnh | CVAT 2.82/2.83 của lớp không có tính năng này (bản guideline .docx viết cho một bản CVAT khác) | Dùng ảnh camera để nhận loại vật và đầu, đuôi xe; đo kích thước ở Top, Side, Front; xem cuboid trên 7 ảnh camera bằng `python scripts/lab.py preview` |
| Tưởng "phía trước là +x" hoặc "y là bên trái" | Nhớ hệ tọa độ khác (KITTI, ROS) | Xem cam01: ảnh trước trùng hướng −y. x dương là trái, y dương là sau |
| Mất cuboid sau khi đóng tab | Chưa Save | Save sau mỗi frame (`Ctrl+S`, macOS `Cmd+S`) |

## 5. Bảng A, tự kiểm, nộp bài

| Triệu chứng | Nguyên nhân | Cách gỡ |
|---|---|---|
| `Bảng A trống` hoặc thiếu cuboid | Chưa Save trong CVAT, hoặc vẽ bằng Track | Save; cuboid Track thì vẽ lại bằng Shape; chạy lại `report` |
| `Chưa có submission/D13-…-bangA.csv` khi chạy `preview` hoặc `selfcheck` | Chưa chạy `report` | Chạy `python scripts/lab.py report` trước, hoặc chạy `sync` |
| `length` và `width` đổi chỗ ở **mọi** xe dù mũi tên đỏ dọc thân xe | Thứ tự trục của CVAT khác với công cụ | Báo coach. Không vẽ lại |
| Excel mở CSV ra chữ lạ hoặc dồn một cột | Excel đoán sai bảng mã hoặc dấu phân cách | Data → From Text/CSV, chọn **65001: Unicode (UTF-8)**, phân cách dấu phẩy. Hoặc mở bằng Numbers. Chỉ mở để đọc |
| Excel hiện `-1.7` thành ngày tháng hoặc số sai | Vùng miền dùng dấu phẩy thập phân | Nhập qua From Text/CSV như trên; **không lưu đè** file CSV gốc |
| `check_submission.py` báo bảng A `đã bị lưu lại bằng bảng tính`, `không giống bản do report sinh ra`, hoặc `cột khác` | Đã lưu đè CSV từ Excel hoặc sửa tay; công cụ chấm của coach không đọc được file như vậy | Chạy lại `python scripts/lab.py sync` để sinh lại, rồi `pack` |
| `check_submission.py` báo phiếu tự kiểm không khớp bảng A | Sửa cuboid rồi chạy `report` mà chưa chạy `selfcheck` | Chạy `python scripts/lab.py sync` |
| `check_submission.py` báo `chưa có work/...-nop.zip` hoặc zip `chứa bản cũ` | Chưa chạy `pack`, hoặc chạy `sync` sau `pack` | Chạy `python scripts/lab.py pack`, nộp lại file zip mới |
| `check_submission.py` báo repo đang theo dõi file dữ liệu, ảnh, bảng A | Đã `git add -f`, hoặc sửa `.gitignore` | `git rm --cached <file>`, commit lại. Rồi làm theo dòng dưới nếu file đã nằm trong một commit trước |
| `check_submission.py` báo `lịch sử commit vẫn còn` file không được public | File đã vào một commit; `git rm --cached` chỉ gỡ ở commit mới, `git push` vẫn đẩy commit cũ | **Chưa push**: `git reset --soft origin/main`, `git rm --cached <file>`, commit lại. **Đã push**: chuyển repo sang Private ngay (Settings → Danger Zone → Change visibility) và báo coach; đừng tự force-push |
| `check_submission.py` báo `không phải git repo` | Tải repo bằng nút Download ZIP | `git clone` repo của bạn ([SETUP.md](SETUP.md) mục 3), chép `configs/lab.ini` và `submission/` sang, nộp bằng `git push` |
| `selfcheck` cờ gần hết người đi bộ | Ngưỡng của công cụ chặt với vật nhỏ | Xem lại từng hộp; hộp đúng thì giữ và ghi một dòng lý do vào báo cáo ([SELF_CHECK.md](SELF_CHECK.md)) |
