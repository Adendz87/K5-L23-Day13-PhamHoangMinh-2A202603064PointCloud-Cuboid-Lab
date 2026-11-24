# Tự kiểm: `preview`, `selfcheck` và bảng A

Hai lệnh `preview` và `selfcheck` chỉ đọc point cloud, ảnh camera, `calib.json` và cuboid của chính bạn trong bảng A. Chúng **không biết đáp án** và **không tính điểm**.

## 1. `preview` — nhìn cuboid của bạn trên ảnh camera

```bash
python scripts/lab.py preview
```

Mỗi frame ra một ảnh trong thư mục `work/xem/`: 7 ảnh camera và một ảnh nhìn từ trên xuống, có cuboid của bạn vẽ đè kèm số thứ tự, màu theo class. Ảnh nhìn từ trên xuống phủ 35 m quanh xe (vòng 10, 20, 30 m), đầu xe của bạn hướng lên; mỗi cuboid có một vạch từ tâm tới cạnh đầu xe. Vật xa hơn 35 m chỉ thấy trên ảnh camera. Tìm:

- Hộp lệch khỏi vật trên ảnh, hoặc đặt vào chỗ không có vật.
- Hộp ngược đầu, hoặc dài và rộng đổi chỗ.
- Hộp quá to hoặc quá nhỏ so với vật.
- Class không khớp thứ bạn thấy trên ảnh (bán tải gán Car, người dắt xe gán Cyclist).

Lệnh cũng báo số hộp không camera nào thấy. Điều này bình thường với vật bị che hoặc nằm ở góc mù giữa các camera (7 camera không phủ kín 360°, còn LiDAR thì có).

## 2. `selfcheck` — soát từng cuboid bằng point cloud

```bash
python scripts/lab.py selfcheck
```

Kết quả ghi vào `submission/D13-<MÃ SỐ>-tukiem.csv` với các cột `frame, idx, label, dist_m, points_in, ground_gap_m, flags`:

- `points_in`: số điểm LiDAR nằm trong cuboid. Dùng cho câu mật độ ở `REPORT.md` mục 5.
- `ground_gap_m`: đáy cuboid trừ độ cao mặt đường ước từ các điểm quanh hộp (trong vòng khoảng 4 m). Dương là đáy cao hơn mặt đường, âm là đáy thấp hơn. Trống nếu quanh hộp quá ít điểm mặt đường.
- `flags`: các cảnh báo dưới đây, cách nhau bằng dấu `;`.

| Cảnh báo | Nghĩa là | Việc cần làm |
|---|---|---|
| Hộp rỗng hoặc rất ít điểm (dưới 5 điểm) | Hộp đặt lệch, hoặc vật rất thưa | Mở lại trên CVAT. Nếu vật thật sự thưa, áp quy tắc 15–20%. Rất nhiều hộp rỗng cùng lúc thì kiểm lại dữ liệu ([COMMON_ERRORS.md](COMMON_ERRORS.md) mục 2) |
| Đáy lơ lửng (cao hơn mặt đường quá khoảng 0,45 m) hoặc chìm (thấp hơn quá khoảng 0,25 m) | Đáy lệch khỏi mặt đường quanh hộp | Chỉnh ở Side và Front |
| Kích thước ngoài khoảng của class | Dài, rộng hoặc cao ngoài khoảng rộng của công cụ (ví dụ Car dài 3–6 m). Khoảng này rộng hơn bảng 4.3 | So với bảng 4.3; kiểm class. Xe tải nhỏ, xe ba bánh có thể bị cờ dù đúng |
| `length < width` | Mũi tên yaw có thể đang nằm ngang thân xe | Xoay 90° để mũi tên đỏ dọc thân xe, rồi kéo lại để cạnh dọc mũi tên là cạnh dài; kiểm lại ở Top |
| Quá chật: nhiều điểm sát ngay ngoài mép | Hộp nhỏ hơn vật, hoặc chạm vật bên cạnh | Nới hộp cho bao trọn vật; nếu điểm đó là của vật bên cạnh thì giữ |
| Chồng lên hộp khác | Vẽ trùng một vật, hoặc hai hộp lấn nhau | Xóa hộp trùng hoặc tách lại |

**Cảnh báo là gợi ý để xem lại, không phải lỗi chắc chắn.** Trên nhãn chuẩn của chính bộ VF, hộp đúng vẫn bị cờ khoảng 7% với Car và 22–28% với các class nhỏ (người đi bộ, xe hai bánh). Hộp sai có thể không bị cờ. Đừng chỉnh hộp cho hết cờ mà không nhìn lại point cloud.

Yêu cầu của bài lab: xem lại mọi cuboid có cờ, **sửa ít nhất 2 cuboid** trên CVAT, Save, chạy lại `python scripts/lab.py sync`. Ghi vào `REPORT.md` mục 5 cờ nào bạn giữ nguyên và vì sao.

## 3. Các cột của bảng A

| Cột | Ý nghĩa |
|---|---|
| `student` | Mã số của bạn |
| `frame`, `idx`, `label` | Tên frame, số thứ tự cuboid trong frame, class |
| `x`, `y`, `z` | Tâm cuboid theo hệ VF (x trái, y sau, z lên), mét |
| `length`, `width`, `height` | Dài (dọc mũi tên yaw), rộng, cao, mét |
| `yaw_rad`, `yaw_deg` | Góc yaw, `yaw_deg` trong 0–360° |
| `z_bottom` | z − height/2, độ cao đáy cuboid |
| `dist_m`, `dist_bin` | √(x² + y²) và khoảng cách theo bin: 0-10, 10-20, 20-30, 30-50, và >=50 (xa hơn 50 m, không được chấm) |
| `az_deg` | Góc phương vị của tâm: 0° thẳng phía trước, dương lệch trái, âm lệch phải, ±180° phía sau |
| `occluded` | 1 nếu bạn đã bật occluded |
