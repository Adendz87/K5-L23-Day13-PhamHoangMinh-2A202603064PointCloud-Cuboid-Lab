# Quy tắc làm bài

## Hình thức
**Bài cá nhân.** Mỗi người một mã số, một task CVAT `D13-<MÃ SỐ>`, một repo (tạo từ repo đề bằng **Use this template**). Commit dưới tên của bạn. Ngồi theo cặp để đổi kiểm ở cuối buổi.

## Sản phẩm là của bạn
- Mọi cuboid trong task `D13-<MÃ SỐ>` do **bạn** vẽ. Không vẽ hộ, không nhờ vẽ hộ, không dùng mã số của người khác để tạo task.
- Mỗi mã số nhận 10 frame khác nhau. Được bàn với bạn về cách hiểu guideline, ca khó, lỗi CVAT; gọi ca khó bằng **tên frame và vị trí** ("s02f07, xe trắng bên trái khoảng 10 m").
- Frame mượn cho phần bốn hiện tượng phải **ghi rõ mượn của ai** trong `submission/REPORT.md` mục 4.
- Được dùng AI để hỏi về lệnh Python, PowerShell, Terminal, Docker, cách dùng CVAT, hoặc một khái niệm (yaw, BEV, intensity…).
  **Không** đưa ảnh camera, ảnh chụp màn hình hay file point cloud cho AI. Không nhờ AI vẽ cuboid, viết dòng nhận xét hay điền số.
  Ghi 3 dòng (công cụ, câu hỏi chính, bạn dùng kết quả thế nào) trong `REPORT.md` mục 6, hoặc ghi "không dùng".

## Tính trung thực của số liệu
- **Không sửa tay** `submission/*-bangA.csv` và `submission/*-tukiem.csv`. Bảng A phải khớp task CVAT của bạn. Muốn đổi số thì sửa cuboid trên CVAT, Save, rồi chạy lại `python scripts/lab.py sync`.
- Không mở bảng A bằng Excel rồi **lưu đè**: Excel đổi định dạng số và làm hỏng file. Chỉ mở để đọc.
- Không sửa các file "ĐÃ VIẾT SẴN": `cvat_lab/*.py`, `scripts/lab.py`, `scripts/check_submission.py` (`check_submission.py` so sha1; coach chấm bằng bản gốc của mình).
- Không chỉnh cuboid chỉ để tắt cờ của `selfcheck`. Cờ không tính điểm; cuboid đúng vẫn có thể bị cờ. Giữ cuboid bạn tin là đúng và ghi lý do vào `REPORT.md` mục 5.
- Vật không đủ cơ sở thì **không đoán**: bỏ qua và ghi vào báo cáo. Báo cáo trung thực "chưa chắc" vẫn được điểm tốt. Điều bị trừ là số trong báo cáo không khớp bảng A, hoặc khẳng định nguyên nhân của một hiện tượng khi chỉ có giả thuyết.
- Các bạn vẽ giống nhau chỉ cho thấy **nhất quán**, không chứng minh cuboid **đúng**. Guideline và coach là căn cứ phân xử.
- Sau hạn nộp, không sửa cuboid trong task. Lỗi phát hiện thêm thì ghi vào `REPORT.md` mục 6.

## Dữ liệu và giấy phép
- Dữ liệu VF là dữ liệu lái xe thực tế của dự án, **chỉ dùng trong lớp**. Ảnh camera có người và biển số thật.
- `data/data-VF/` chỉ nằm trên máy bạn và trong CVAT của lớp (CVAT local hoặc máy chủ coach phát). Không tải lên Drive cá nhân, GitHub, chatbot AI, hay CVAT online.
- **Repo của bạn là public**: không commit point cloud (`.bin`, `.pcd`), ảnh camera, ảnh xem trước (`work/xem/`), hay ảnh chụp màn hình. `.gitignore` đã chặn; đừng sửa các dòng đó, đừng dùng `git add -f`.
- Ảnh chụp màn hình của báo cáo để trong `submission/images/` và **nộp qua LMS** (`python scripts/lab.py pack`). Không gửi vào nhóm chat hay mạng xã hội.
- Bảng A và phiếu tự kiểm chỉ chứa số của cuboid bạn vẽ, nên được commit.
- Hết khóa, xóa `data/data-VF/` và `work/` trên máy.

## Mật khẩu
- Mật khẩu CVAT chỉ nhập tay khi lệnh hỏi, hoặc đặt biến môi trường `CVAT_PASSWORD` cho cửa sổ terminal đang mở ([docs/COMMANDS.md](docs/COMMANDS.md)).
- **Không ghi mật khẩu vào `configs/lab.ini` hay bất kỳ file nào**, không dán vào báo cáo, không commit `.env`, token, API key.
- Không dùng lại mật khẩu email hay LMS cho CVAT.

## Không tự xóa task
- `python scripts/lab.py task --replace` xóa task cùng mọi cuboid. Chỉ dùng khi chưa vẽ gì, hoặc khi coach bảo.
- Không chạy `docker compose down -v` cho tới khi đã có điểm.

## Git
- Commit nhỏ, thông điệp rõ (sau frame 1, sau giờ nghỉ, sau tự kiểm, sau báo cáo là tốt). Nộp theo commit cuối trước hạn.
- Không commit `work/`, `.venv/`, `data/data-VF/`.
