# Hướng dẫn làm lab (5 bước)

Bài **cá nhân**, buổi thực hành **16:00–20:00** (10' điểm danh, 195' làm bài, 15' nghỉ, 20' dự phòng). Cài đặt và tải dữ liệu làm **trước buổi học** ([docs/SETUP.md](docs/SETUP.md), [docs/CVAT_SETUP.md](docs/CVAT_SETUP.md)). Mốc giờ ở [CHECKPOINTS.md](CHECKPOINTS.md). Lệnh chạy **từ thư mục gốc repo**, đã kích hoạt `.venv`.
Quy tắc: [RULES.md](RULES.md) · Chấm điểm: [RUBRIC.md](RUBRIC.md) · Nộp: [SUBMISSION.md](SUBMISSION.md).

| Bước | Việc | Lệnh chính | Sản phẩm | Thời gian |
|---|---|---|---|---|
| 1 | Chuẩn bị, tạo task (P0) | `python scripts/lab.py dry`, `python scripts/lab.py task` | task `D13-<MÃ SỐ>` | ~15' |
| 2 | **Đọc frame** năm bước (T1) | — (làm trên CVAT) | `REPORT.md` §2, 4 ảnh | ~25' |
| 3 | **Vẽ cuboid** (T2, T3) | `python scripts/lab.py report` | 60–70 cuboid, `REPORT.md` §3, 3 ảnh | ~90' |
| 4 | Săn bốn hiện tượng (T4) | — (làm trên CVAT) | `REPORT.md` §4, 4 ảnh | ~25' |
| 5 | Đọc số, tự kiểm, báo cáo, nộp (T5) | `python scripts/lab.py sync`, `python scripts/check_submission.py` | bảng A, phiếu tự kiểm, `REPORT.md` | ~45' |

Lệnh `python scripts/lab.py ...` giống nhau trên Windows và macOS. macOS có thể gõ tắt `make dry`, `make task`, `make sync`, `make check`. Lệnh riêng từng hệ điều hành: [docs/COMMANDS.md](docs/COMMANDS.md).

## Bước 1 — Chuẩn bị, tạo task (~15')

Mở `configs/lab.ini`, điền `student` (mã số của bạn) và `cvat_user` (tên đăng nhập CVAT). Không ghi mật khẩu vào file. Rồi:

```bash
python scripts/lab.py dry      # in 10 frame của bạn, mỗi frame camera=7; không nối CVAT
python scripts/lab.py task     # tạo task D13-<MÃ SỐ>; hỏi mật khẩu CVAT, màn hình không hiện ký tự
```

Mở đường dẫn task lệnh in ra bằng Chrome hoặc Edge, vào job. Bạn phải thấy point cloud và ảnh camera.
Tên frame `s02f07` nghĩa là sequence 02, frame chỉ số 7 (đếm từ 0). Chạy lại `task` khi đã có task chỉ in lại đường dẫn cũ.

> **Không dùng `--replace` nếu đã vẽ gì**: `python scripts/lab.py task --replace` xóa task cùng mọi cuboid rồi tạo lại.

Đọc [docs/COORDINATES.md](docs/COORDINATES.md) (3'): **x trái, y sau, z lên; phía trước xe là −y**. Điền `submission/REPORT.md` mục 1 phần thông tin.

## Bước 2 — Đọc frame năm bước (~25', chưa vẽ)

Đi kỹ trên **2 frame đầu**, khoảng 8 phút mỗi frame. Lướt 8 frame còn lại, khoảng 1 phút mỗi frame.

| # | Bước đọc | Trả lời câu gì |
|---|---|---|
| 1 | **Gốc và trục** | Mở Top. Dựa vào cam01 (nhìn về phía trước), phía nào của Top là phía trước (−y)? +x, +y chỉ về đâu? |
| 2 | **Mặt đất** | Mở Side. Đường phẳng hay dốc? Thấp hơn LiDAR khoảng bao nhiêu mét? |
| 3 | **Tầm và góc nhìn** | Vật xa nhất còn nhận ra cách bao xa? Phần nào ảnh camera không thấy? |
| 4 | **Ảnh camera** | Đổi giữa các camera. 3 điều chỉ camera cho biết, 3 điều chỉ LiDAR cho biết |
| 5 | **Quét cảnh** | Có những loại vật nào? Ít nhất một cụm điểm bạn chưa đọc được |

Chụp một ảnh view 3D và một ảnh Top cho mỗi frame đọc kỹ; trên ảnh Top đánh dấu phía trước, +x, +y. Điền `REPORT.md` mục 2.
**Vật phía sau và hai bên không có trong ảnh cam01.** Tìm chúng ở Top rồi đối chiếu camera nhìn về hướng đó (cam09 nhìn ra sau).

## Bước 3 — Vẽ cuboid (~90', nghỉ ở giữa)

**3a. Frame 1, có hướng dẫn (35').** Coach demo vẽ một xe. Sau đó là **vòng hiệu chuẩn**: cả lớp vẽ cùng 3 vật trên một frame chung do coach chỉ định, không trao đổi, rồi so cuboid giữa các bạn với nhau. Ba cuboid này không chấm điểm. Các bạn vẽ giống nhau chỉ cho thấy **nhất quán**, chưa chắc **đúng**; guideline và coach mới là căn cứ.

Tiếp theo, trên frame đầu tiên của task, vẽ ba vật mẫu: **(a)** xe con gần nhất, **(b)** một xe buýt hoặc xe tải, **(c)** một người đi bộ hoặc xe hai bánh (frame thiếu loại nào thì lấy ở frame 2). Chụp ảnh từng cuboid. Rồi vẽ tiếp các vật gần đến khi frame 1 có **từ 8 cuboid, nên 10**.

Checklist cho mỗi cuboid ([docs/GUIDELINE.md](docs/GUIDELINE.md)):

1. Class đúng: bán tải là Truck; xe máy có người là Cyclist; người dắt xe là Pedestrian.
2. Bao trọn điểm của vật, gồm phần bị che suy ra được; không bao dư. Dùng **Shape**, không dùng Track.
3. Bật orientation: **mũi tên đỏ chỉ đầu xe**.
4. Đáy chạm mặt đường: kiểm ở Side và Front.
5. Kiểm đủ Top, Side, Front, rồi đối chiếu ảnh camera.
6. So kích thước với bảng 4.3. Vật bị che một phần: bật occluded.
7. Vật rất thưa: thấy khoảng 15–20% thể tích thì vẽ; không đủ cơ sở thì bỏ qua và ghi vào `REPORT.md`.

**3b. Frame 2–10 (55').** Mỗi frame khoảng 6 phút: frame 2–6 trước giờ nghỉ, frame 7–10 sau. **Hết giờ của frame thì sang frame sau, không dồn.** Mỗi frame **từ 5 cuboid, nên 6**, theo thứ tự gần → xa. Quét Top theo vòng tròn quanh xe để không sót vật phía sau và hai bên. Không vẽ xe của chính mình. **Save sau mỗi frame.**

Sau frame 1, kiểm nhanh bằng số:

```bash
python scripts/lab.py report   # -> submission/D13-<MÃ SỐ>-bangA.csv, in số cuboid từng frame
```

Xe con phải có `length` khoảng 3,8–5,3 m và lớn hơn `width`; xe cùng chiều phía trước có `yaw_deg` gần 270°; `z_bottom` khoảng −1,7 m.

## Bước 4 — Săn bốn hiện tượng (~25')

Mỗi hiện tượng cần **một ảnh chụp từ CVAT** và **một dòng**: nguyên nhân (giả thuyết) → thấy gì trên point cloud → việc gán nhãn bị ảnh hưởng thế nào theo guideline.

| # | Hiện tượng | Guideline nói gì |
|---|---|---|
| 1 | Bóng che | Bật occluded, cuboid bao phần suy luận được |
| 2 | Thưa ở xa | Vẽ nếu thấy khoảng 15–20% thể tích; không thì bỏ qua, ghi LOW_VISIBILITY |
| 3 | Phản xạ thấp hoặc ít điểm bất thường | Ghi giả thuyết, không khẳng định |
| 4 | Điểm lạ | Không gán thành vật |

Cách tìm và danh sách frame gợi ý: [docs/PHENOMENA.md](docs/PHENOMENA.md). Frame của bạn thiếu hiện tượng nào thì xem nhờ frame của bạn bên cạnh và **ghi rõ mượn của ai**. Điền `REPORT.md` mục 4.

## Bước 5 — Đọc số, tự kiểm, báo cáo, nộp (~45')

Bấm **Save** trong CVAT, rồi:

```bash
python scripts/lab.py sync     # = report + preview + selfcheck
```

| Lệnh con | Ra file | Dùng để |
|---|---|---|
| `report` | `submission/D13-<MÃ SỐ>-bangA.csv` | 7 tham số, `z_bottom`, `dist_m`, `az_deg` của từng cuboid |
| `preview` | `work/xem/*.jpg` | Nhìn cuboid của bạn trên 7 ảnh camera và ảnh từ trên xuống |
| `selfcheck` | `submission/D13-<MÃ SỐ>-tukiem.csv` | Số điểm trong cuboid, khoảng hở với mặt đường, cảnh báo |

Mở ảnh trong `work/xem/` và danh sách cảnh báo ([docs/SELF_CHECK.md](docs/SELF_CHECK.md)). **Sửa ít nhất 2 cuboid** trên CVAT, Save, chạy lại `sync`.
Cảnh báo là **gợi ý để xem lại**, không phải lỗi chắc chắn và không tính điểm: cuboid đúng vẫn có thể bị cờ, cuboid sai có thể không bị cờ. Đừng chỉnh cho hết cờ mà không nhìn lại point cloud.

Điền `REPORT.md` mục 5 từ bảng A: ba z đáy (z − h/2), khoảng cách gần nhất và xa nhất, kích thước so với bảng 4.3, yaw, và mật độ điểm theo khoảng cách (cột `points_in` của phiếu tự kiểm). Rồi mục 6. Cuối cùng:

```bash
python scripts/check_submission.py    # kiểm bài nộp: hết LỖI mới nộp
python scripts/lab.py pack            # nén 11 ảnh chụp để nộp LMS (ảnh không commit)
```

Sửa hết `LỖI`, đổi dòng tiêu đề README, đối chiếu [SUBMISSION.md](SUBMISSION.md), commit, push, nộp link repo và file zip ảnh.

## Lỗi hay gặp

| Triệu chứng | Cách xử lý |
|---|---|
| `Chưa điền student trong configs/lab.ini` | Điền mã số và tên đăng nhập CVAT vào `configs/lab.ini` |
| `Không thấy sequence_XX/lidar/*.bin` | `data` trong `configs/lab.ini` phải trỏ vào thư mục chứa trực tiếp `sequence_01 … sequence_05` |
| `Thiếu cvat-sdk` / `Thiếu Pillow` | Chưa kích hoạt `.venv`, hoặc chưa `python -m pip install -r requirements.txt` |
| Không nối được CVAT | Mở địa chỉ bằng trình duyệt trước; CVAT local: `docker compose up -d` trong thư mục `cvat` |
| `Đã có task D13-…` | Mở task cũ theo đường dẫn lệnh in ra. Không thêm `--replace` nếu đã vẽ gì |
| `Bảng A trống` hoặc thiếu cuboid | Chưa Save trong CVAT: Save rồi chạy lại `report` |
| Mũi tên ngược đầu xe | Xoay yaw 180°, kiểm lại với ảnh camera |
| Đáy lơ lửng hoặc chìm | Chỉ chỉnh ở Top: chỉnh thêm ở Side và Front, xem `z_bottom` |
| `length` và `width` đổi chỗ ở **mọi** xe dù mũi tên dọc thân xe | Lỗi công cụ, báo coach, không vẽ lại |
| Tưởng "phía trước là +x" | Đang nhớ hệ KITTI/ROS. Xem cam01: ảnh trước trùng hướng −y |

Đầy đủ hơn: [docs/COMMON_ERRORS.md](docs/COMMON_ERRORS.md).

> **Vì sao hôm nay không dùng Track?** Guideline viết cho chuỗi frame liên tiếp, có nội suy và khóa kích thước theo track. 10 frame của bạn lấy rời từ 5 sequence nên không có gì để nội suy. Hôm nay bạn luyện đọc cảnh và vẽ một cuboid cho đúng; track là nội dung Ngày 24–26.
