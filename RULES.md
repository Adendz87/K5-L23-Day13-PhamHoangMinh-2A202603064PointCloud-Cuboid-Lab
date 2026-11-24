# Quy tắc làm bài

## Hình thức
**Bài cá nhân.** Mỗi người một mã số (MSHV), một task CVAT `D13-<MÃ SỐ>` trên CVAT của máy mình, một repo (tạo từ repo đề bằng **Use this template**). Commit dưới tên của bạn. Ngồi theo cặp để đổi kiểm ở cuối buổi.

## Sản phẩm là của bạn
- Mọi cuboid trong task `D13-<MÃ SỐ>` do **bạn** vẽ. Không vẽ hộ, không nhờ vẽ hộ, không dùng mã số của người khác để tạo task. Mã chung của vòng hiệu chuẩn chỉ dùng cho vòng đó và cho Bước 4.
- Mỗi mã số nhận 10 frame, nhưng nhiều frame trùng với bạn khác. Được bàn về cách hiểu guideline, ca khó, lỗi CVAT; gọi ca khó bằng **tên frame và vị trí** ("s02f07, xe trắng bên trái khoảng 10 m"). **Không** gửi, chép hay so file bảng A với nhau. Bảng A của mọi người đều nằm trên repo public: chép cuboid từ bảng A của người khác là gian lận, và coach có thể so trùng giữa các bài. Khi đổi kiểm, chỉ xem trên màn hình.
- Frame mượn cho phần bốn hiện tượng phải **ghi rõ nguồn** trong `submission/REPORT.md` mục 4: task chung, hoặc MSHV của bạn cho mượn.
- Được dùng AI để hỏi về lệnh Python, PowerShell, Terminal, Docker, cách dùng CVAT, hoặc một khái niệm (yaw, BEV, intensity…).
  **Không** đưa cho AI hay dịch vụ ngoài: ảnh camera, ảnh trong `work/xem/`, ảnh chụp màn hình, mọi file trong `data/data-VF/` (kể cả `calib.json`). Không nhờ AI vẽ cuboid, viết dòng nhận xét, đọc bảng A hộ hay điền số.
  Ghi 3 dòng (công cụ, câu hỏi chính, bạn dùng kết quả thế nào) trong `REPORT.md` mục 6, hoặc ghi "không dùng".

## Tính trung thực của số liệu
- **Không sửa tay** bảng A (`submission/D13-<MÃ SỐ>-bangA.csv`) và phiếu tự kiểm (`submission/D13-<MÃ SỐ>-tukiem.csv`). Muốn đổi số thì sửa cuboid trên CVAT, Save, rồi chạy lại `python scripts/lab.py sync`. `check_submission.py` báo LỖI khi bảng A bị sửa tay hoặc lưu lại bằng Excel.
- Không mở bảng A bằng Excel rồi **lưu đè**: chỉ mở để đọc.
- Không sửa các file "ĐÃ VIẾT SẴN": `cvat_lab/*.py`, `scripts/lab.py`, `scripts/check_submission.py` (`check_submission.py` so sha1; coach chấm bằng bản gốc).
- Không chỉnh cuboid chỉ để tắt cờ của `selfcheck`. Cờ không tính điểm; cuboid đúng vẫn có thể bị cờ. Giữ cuboid bạn tin là đúng và ghi lý do vào `REPORT.md` mục 5.
- Vật không đủ cơ sở thì **không đoán**: bỏ qua và ghi vào báo cáo. Báo cáo trung thực "chưa chắc" vẫn được điểm tốt. Điều bị trừ là số trong báo cáo không khớp bảng A, hoặc khẳng định nguyên nhân của một hiện tượng khi chỉ có giả thuyết.
- Các bạn vẽ giống nhau chỉ cho thấy **nhất quán**, không chứng minh cuboid **đúng**. Guideline và coach là căn cứ phân xử.
- Nộp lần đầu trước 19:30, được nộp lại tới **20:00** ([SUBMISSION.md](SUBMISSION.md)). Sau 20:00 không sửa cuboid, không nộp lại; lỗi phát hiện thêm thì ghi vào `REPORT.md` mục 6.

## Dữ liệu và giấy phép
- Dữ liệu VF là dữ liệu lái xe thực tế của dự án, **chỉ dùng trong lớp**. Bạn được cấp vì đã ký cam kết bảo mật. Ảnh camera có người và biển số thật.
- Link tải và mật khẩu giải nén do GV gửi riêng: không chép vào repo, báo cáo hay nhóm chat.
- `data/data-VF/` chỉ nằm trên máy bạn và trong CVAT trên máy bạn. Không tải lên Drive cá nhân, GitHub, chatbot AI, hay CVAT online. Không để repo, dữ liệu, ảnh chụp trong thư mục tự đồng bộ lên mây (OneDrive, iCloud "Desktop & Documents", Google Drive): xem [docs/SETUP.md](docs/SETUP.md) mục 3.
- **Repo của bạn là public**: chứa báo cáo, cấu hình, bảng A và phiếu tự kiểm (chỉ là số đo của cuboid bạn vẽ). Không commit point cloud (`.bin`, `.pcd`), ảnh camera, ảnh xem trước (`work/xem/`), ảnh chụp màn hình, file zip. `.gitignore` đã chặn; đừng sửa các dòng đó, đừng dùng `git add -f`.
- Ảnh chụp màn hình **nộp qua LMS** trong file zip (`python scripts/lab.py pack`). Không gửi vào nhóm chat hay mạng xã hội.
- Báo cáo nằm trên repo public: mô tả chung (loại vật, màu, trái hay phải, cách khoảng bao nhiêu mét). **Không** chép biển số, chữ trên biển hiệu hay biển chỉ đường, tên đường, địa danh, đặc điểm nhận dạng một người. Nhắc tới bạn khác thì ghi MSHV, không ghi họ tên.
- Phiếu hồ sơ lỗi coach phát (nếu có) chỉ dành cho bạn: không commit, không chia sẻ.
- Hết khóa, xóa `data/data-VF/`, `work/`, file `Data-VF.zip` trong Downloads, và ảnh chụp còn sót ở Desktop, Pictures.

## Mật khẩu
- Mật khẩu CVAT chỉ nhập tay khi lệnh hỏi, hoặc đặt biến môi trường `CVAT_PASSWORD` cho cửa sổ terminal đang mở theo đúng lệnh ở [docs/COMMANDS.md](docs/COMMANDS.md) mục 6.
- **Không ghi mật khẩu vào `configs/lab.ini` hay bất kỳ file nào**, không dán vào báo cáo, không commit `.env`, token, API key.
- Không gõ mật khẩu thẳng vào dòng lệnh (ví dụ `tar --passphrase …`, `$env:CVAT_PASSWORD = "…"`): nó nằm lại trong lịch sử lệnh. Để lệnh tự hỏi.
- Không dùng lại mật khẩu email hay LMS cho CVAT.

## Không tự xóa task
- `python scripts/lab.py task --replace` xóa task cùng mọi cuboid. Chỉ dùng khi chưa vẽ gì, hoặc khi coach bảo.
- Không chạy `docker compose down -v` cho tới khi đã có điểm.

## Git
- Commit nhỏ, thông điệp rõ (sau frame 1, sau giờ nghỉ, sau tự kiểm, sau báo cáo là tốt). Bản được chấm là commit cuối trên GitHub và file zip cuối trên LMS trước 20:00.
- Không commit `work/`, `.venv/`, `data/data-VF/`, file trong `submission/` ngoài `REPORT.md`, bảng A và phiếu tự kiểm của bạn.
