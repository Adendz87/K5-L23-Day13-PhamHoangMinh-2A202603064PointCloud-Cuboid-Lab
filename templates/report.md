# Báo cáo Lab Ngày 13 — Point cloud VF và cuboid CVAT 3D

> Chép file này thành `<MÃ SỐ>-report.md` trong thư mục nộp rồi điền dần trong buổi. Mọi con số ghi kèm đơn vị (m, °). Ảnh để trong `images/`, đặt tên theo SUBMISSION.md.

## 0. Thông tin

- Họ tên:
- Mã số:
- Task: D13-
- 10 frame: ___, ___, ___, ___, ___, ___, ___, ___, ___, ___
- Hệ điều hành / trình duyệt:
- CVAT (local hay máy chủ lớp, phiên bản):
- Bạn ngồi cạnh (đổi kiểm):

## 1. Cách dùng CVAT

Ba dòng, viết bằng lời của bạn: cách đổi view, cách vẽ một cuboid, cách bật mũi tên yaw và xem cuboid trên ảnh camera.

1.
2.
3.

## 2. Đọc frame (T1)

Hai frame đọc kỹ:

| Frame | Phía trước xe ở cạnh nào của view Top; +x, +y chỉ về đâu (nói bằng lời) | Mặt đường (phẳng/dốc; thấp hơn LiDAR khoảng bao nhiêu m) | Vật xa nhất đọc được (ước, m) | Loại vật thấy | Vật phía sau hoặc hai bên | Cụm chưa đọc được |
|---|---|---|---|---|---|---|
| s__f__ |  |  |  |  |  |  |
| s__f__ |  |  |  |  |  |  |

Ảnh: `images/t1-s__f__-3d.png`, `images/t1-s__f__-top.png`, `images/t1-s__f__-3d.png`, `images/t1-s__f__-top.png`

Chỉ camera cho biết: 1) ___ 2) ___ 3) ___

Chỉ LiDAR cho biết: 1) ___ 2) ___ 3) ___

Tám frame lướt:

| Frame | Phía trước ở cạnh nào của view Top | Điều lạ (nếu có) |
|---|---|---|
| s__f__ |  |  |
| s__f__ |  |  |
| s__f__ |  |  |
| s__f__ |  |  |
| s__f__ |  |  |
| s__f__ |  |  |
| s__f__ |  |  |
| s__f__ |  |  |

## 3. Cuboid đầu tiên (T2)

| Vật | Frame, idx | Class | Mũi tên yaw đúng hướng? | Đáy chạm đường? | Đã kiểm Top/Side/Front + ảnh? | Kích thước nằm trong bảng 4.3? |
|---|---|---|---|---|---|---|
| (a) xe con gần |  |  |  |  |  |  |
| (b) xe buýt hoặc xe tải |  |  |  |  |  |  |
| (c) người đi bộ hoặc xe hai bánh |  |  |  |  |  |  |

Ảnh: `images/t2-a-car.png`, `images/t2-b-bus-truck.png`, `images/t2-c-ped-cyclist.png`

Vòng hiệu chuẩn: cuboid của tôi lệch so với các bạn ở điểm nào, cả lớp chốt cách hiểu nào?

Vật bỏ qua vì không đủ cơ sở (frame, vị trí, mô tả, loại nghi vấn):

-

## 4. Bốn hiện tượng chất lượng (T4)

| Hiện tượng | Frame / ảnh | Nguyên nhân (giả thuyết) | Thấy gì trên point cloud | Hệ quả khi gán (theo guideline) |
|---|---|---|---|---|
| 1. Bóng che | `images/t4-1-bong-che.png` |  |  |  |
| 2. Thưa ở xa | `images/t4-2-thua-o-xa.png` |  |  |  |
| 3. Phản xạ thấp / ít điểm bất thường | `images/t4-3-phan-xa-thap.png` |  |  |  |
| 4. Điểm lạ | `images/t4-4-diem-la.png` |  |  |  |

Frame mượn của bạn khác (nếu có, ghi mượn của ai):

## 5. Số từ cuboid của tôi (T5, từ bảng A)

Tổng số cuboid: ___ · Số cuboid từng frame: ___

| Cuboid (frame, idx, class) | z | h | z đáy = z − h/2 | dist_m | r = √(x²+y²+z²) | yaw_deg | Nhận xét (lơ lửng, chìm, chạm đường) |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |

Cuboid gần nhất: ___ (dist_m = ___ , r = ___) · Cuboid xa nhất: ___ (dist_m = ___ , r = ___)

Kích thước so với bảng 4.3:

| Vật | l | w | h | Chiều nào ngoài khoảng, vì sao |
|---|---|---|---|---|
| Người đi bộ hoặc xe hai bánh |  |  |  |  |
| Xe con |  |  |  |  |

Hướng: một xe cùng chiều phía trước có yaw_deg = ___ ; một xe ngược chiều (nếu có) có yaw_deg = ___

Mật độ theo khoảng cách (4 cuboid, số điểm lấy từ cột `points_in` của phiếu tự kiểm):

| Cuboid (frame, idx, class) | dist_m | Số điểm |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

Quy luật: "xa gấp ___ lần thì số điểm còn khoảng ___"

Tự kiểm (`preview`, `check`):

- Số cuboid có cảnh báo: ___ / ___
- Hai cuboid tôi đã sửa (frame, idx, sửa gì):
- Cảnh báo tôi giữ nguyên và lý do:

## 6. "… để làm gì?"

Hai câu, nói từ phía model sẽ học trên nhãn này:

1. Vì sao nhãn 3D đo bằng mét, không phải pixel?
2. Vì sao vật thưa điểm cần quy tắc riêng?

## 7. Điều còn chưa chắc (ghi chú tự do, không chấm)

-
