# Tự kiểm: `preview`, `check` và bảng A

Ba thứ này chỉ đọc point cloud, ảnh camera, `calib.json` và cuboid của chính bạn. Chúng **không biết đáp án** và **không tính điểm**.

## 1. `preview` — nhìn cuboid của bạn trên ảnh camera

```bash
python scripts/lab.py preview
```

Mỗi frame ra một ảnh trong thư mục `work/xem/`: 7 ảnh camera và một ảnh nhìn từ trên xuống, có cuboid của bạn vẽ đè kèm số thứ tự và class. Tìm:

- Hộp lệch khỏi vật trên ảnh, hoặc đặt vào chỗ không có vật.
- Hộp ngược đầu, hoặc dài và rộng đổi chỗ.
- Hộp quá to hoặc quá nhỏ so với vật.
- Class không khớp thứ bạn thấy trên ảnh (bán tải gán Car, người dắt xe gán Cyclist).

Lệnh cũng báo số hộp không camera nào thấy. Điều này bình thường với vật bị che hoặc ở góc mù giữa các camera.

## 2. `selfcheck` — soát từng cuboid bằng point cloud

```bash
python scripts/lab.py selfcheck
```

Kết quả ghi vào `submission/D13-<MÃ SỐ>-tukiem.csv` với các cột `frame, idx, label, dist_m, points_in, ground_gap_m, flags`. Cột `points_in` là số điểm LiDAR trong cuboid; bạn dùng nó cho câu mật độ ở `REPORT.md` mục 5. Cột `flags` có thể báo:

| Cảnh báo | Nghĩa là | Việc cần làm |
|---|---|---|
| Hộp rỗng hoặc quá ít điểm | Hộp đặt lệch, hoặc vật rất thưa | Mở lại trên CVAT. Nếu vật thật sự thưa, áp quy tắc 15–20% |
| Đáy lơ lửng hoặc chìm | Đáy lệch khỏi mặt đường quanh hộp | Chỉnh ở Side và Front |
| Kích thước ngoài khoảng của class | Dài, rộng hoặc cao bất thường | So với bảng 4.3; kiểm class |
| `length < width` | Mũi tên yaw có thể đang nằm ngang thân xe | Xoay 90° |
| Hộp quá chật | Nhiều điểm của vật nằm sát mép ngoài hộp | Nới hộp cho bao trọn vật |
| Hai hộp chồng nhau | Vẽ trùng một vật, hoặc hai hộp lấn nhau | Xóa hộp trùng hoặc tách lại |

**Cảnh báo là gợi ý để xem lại, không phải lỗi chắc chắn.** Hộp đúng vẫn có thể bị cờ, nhất là vật bị che, người đi bộ, xe tải. Hộp sai có thể không bị cờ. Đừng chỉnh hộp cho hết cờ mà không nhìn lại point cloud.

Yêu cầu của bài lab: xem lại mọi cuboid có cờ, **sửa ít nhất 2 cuboid** trên CVAT, Save, chạy lại `python scripts/lab.py sync`. Ghi vào `REPORT.md` mục 5 cờ nào bạn giữ nguyên và vì sao.

## 3. Các cột của bảng A

| Cột | Ý nghĩa |
|---|---|
| `frame`, `idx`, `label` | Tên frame, số thứ tự cuboid trong frame, class |
| `x`, `y`, `z` | Tâm cuboid theo hệ VF (x trái, y sau, z lên), mét |
| `length`, `width`, `height` | Dài (dọc mũi tên yaw), rộng, cao, mét |
| `yaw_rad`, `yaw_deg` | Góc yaw, `yaw_deg` trong 0–360° |
| `z_bottom` | z − height/2, độ cao đáy cuboid |
| `dist_m`, `dist_bin` | √(x² + y²) và khoảng cách theo bin: 0–10, 10–20, 20–30, 30–50 |
| `az_deg` | Góc phương vị của tâm: 0° thẳng phía trước, dương lệch trái, âm lệch phải, ±180° phía sau |
| `occluded` | 1 nếu bạn đã bật occluded |
