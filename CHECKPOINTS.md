# CHECKPOINTS — các mốc tự kiểm trong buổi

Lệnh đầy đủ cho Windows và macOS ở [COMMANDS.md](COMMANDS.md). Chạy mọi lệnh từ thư mục gốc repo, đã kích hoạt `.venv`.

Ba lệnh tự kiểm chỉ đọc point cloud, ảnh camera, `calib.json` và cuboid của chính bạn. Chúng **không biết đáp án** và **không tính điểm**.

## Checkpoint 0 — 16:25 (sau P0)

```bash
python cvat_lab/vf_cvat.py day13 --student <MÃ SỐ> --data data-VF --dry-run
```

- Lệnh in đủ 10 frame, mỗi frame `camera=7`.
- Trên CVAT có task `D13-<MÃ SỐ>`, mở job thấy point cloud và ảnh camera.
- File báo cáo đã có mục 0 (mã số, task, 10 frame).

## Checkpoint A — 16:50 (sau T1)

Không có lệnh. Coach hỏi từng bạn trên view Top của frame đầu:

- Phía trước xe (−y) nằm ở cạnh nào của view Top?
- +x (bên trái xe) chỉ về đâu?
- Có vật nào ở phía sau hoặc hai bên mà cam01 không thấy?

Trả lời sai thì quay lại [GUIDE.md](GUIDE.md) mục 2.1 trước khi vẽ. Sai trục thì mọi cuboid sau đó đều sai hướng.

## Checkpoint B — 17:25 (sau T2, frame 1)

Bấm **Save**, rồi:

```bash
python cvat_lab/vf_cvat.py report d13 --student <MÃ SỐ> --host http://localhost:8080 --user <tên> --out ./nop
```

Mở `nop/D13-<MÃ SỐ>-bangA.csv` và kiểm các cuboid của frame 1:

| Kiểm | Đúng khi | Nếu sai |
|---|---|---|
| Số cuboid frame 1 | ≥ 8 | Vẽ thêm vật gần |
| `length` của xe con | khoảng 3,8–5,3 m và **lớn hơn** `width` | Mũi tên yaw đang nằm ngang thân xe: xoay 90° |
| `yaw_deg` của xe cùng chiều phía trước | gần 270° | Gần 90° là ngược đầu: xoay 180° |
| `z_bottom` | khoảng −1,7 m, lệch không quá 0,3 m | Lơ lửng hoặc chìm: chỉnh ở Side và Front |

Nếu `length` và `width` của **mọi** xe đều đổi chỗ dù mũi tên đỏ đã dọc thân xe, báo coach. Đó là lỗi công cụ, bạn không cần vẽ lại.

## Checkpoint C — 19:00 (sau T3, trước T5)

Save, chạy lại `report`, rồi chạy hai lệnh tự kiểm.

### `preview` — nhìn cuboid của bạn trên ảnh camera

```bash
python cvat_lab/vf_cvat.py preview d13 --student <MÃ SỐ> --data data-VF
```

Mỗi frame ra một ảnh trong thư mục `xem/`: 7 ảnh camera và một ảnh nhìn từ trên xuống, có cuboid của bạn vẽ đè kèm số thứ tự và class. Tìm:

- Hộp lệch khỏi vật trên ảnh, hoặc đặt vào chỗ không có vật.
- Hộp ngược đầu, hoặc dài và rộng đổi chỗ.
- Hộp quá to hoặc quá nhỏ so với vật.
- Class không khớp thứ bạn thấy trên ảnh (bán tải gán Car, người dắt xe gán Cyclist).

Lệnh cũng báo số hộp không camera nào thấy. Điều này bình thường với vật bị che hoặc ở góc mù giữa các camera.

### `check` — soát từng cuboid bằng point cloud

```bash
python cvat_lab/vf_cvat.py check d13 --student <MÃ SỐ> --data data-VF
```

Kết quả ghi vào `nop/D13-<MÃ SỐ>-tukiem.csv` với các cột `frame, idx, label, dist_m, points_in, ground_gap_m, flags`. Cột `points_in` là số điểm LiDAR trong cuboid; bạn dùng nó cho câu mật độ ở T5. Cột `flags` có thể báo:

| Cảnh báo | Nghĩa là | Việc cần làm |
|---|---|---|
| Hộp rỗng hoặc quá ít điểm | Hộp đặt lệch, hoặc vật rất thưa | Mở lại trên CVAT. Nếu vật thật sự thưa, áp quy tắc 15–20% |
| Đáy lơ lửng hoặc chìm | Đáy lệch khỏi mặt đường quanh hộp | Chỉnh ở Side và Front |
| Kích thước ngoài khoảng của class | Dài, rộng hoặc cao bất thường | So với bảng 4.3; kiểm class |
| `length < width` | Mũi tên yaw có thể đang nằm ngang thân xe | Xoay 90° |
| Hộp quá chật | Nhiều điểm của vật nằm sát mép ngoài hộp | Nới hộp cho bao trọn vật |
| Hai hộp chồng nhau | Vẽ trùng một vật, hoặc hai hộp lấn nhau | Xóa hộp trùng hoặc tách lại |

**Cảnh báo là gợi ý để xem lại, không phải lỗi chắc chắn.** Hộp đúng vẫn có thể bị cờ, nhất là vật bị che, người đi bộ, xe tải. Hộp sai có thể không bị cờ. Đừng chỉnh hộp cho hết cờ mà không nhìn lại point cloud.

Yêu cầu của checkpoint: xem lại mọi cuboid có cờ, **sửa ít nhất 2 cuboid** trên CVAT, Save, chạy lại `report` rồi `check`. Ghi vào báo cáo cờ nào bạn giữ nguyên và vì sao.

## Lần cuối — 19:30 (trước khi nộp)

1. Save trong CVAT.
2. Chạy lại `report`. Dòng `Đã ghi … (N cuboid)` phải báo tổng **từ 50 cuboid**; các dòng bên dưới cho số cuboid từng frame: mỗi frame từ 5, frame 1 từ 8.
3. Chạy lại `check` để phiếu tự kiểm khớp bảng A mới nhất.
4. Đổi máy với bạn bên cạnh: mỗi người kiểm lại **hai con số** trong mục 5 báo cáo của bạn kia (một z đáy, một khoảng cách r).
5. Đóng gói theo [SUBMISSION.md](SUBMISSION.md).

## Không chạy được Python?

Báo coach ngay ở P0. Bạn vẫn vẽ được trên CVAT nếu coach hoặc bạn bên cạnh tạo task giúp bằng mã số của bạn. Mật khẩu CVAT do bạn tự nhập.
