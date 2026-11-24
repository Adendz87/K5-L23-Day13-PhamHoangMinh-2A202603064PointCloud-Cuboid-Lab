# Dữ liệu

Nguồn: **Dữ liệu VF**, dữ liệu lái xe thực tế của dự án, do ban đào tạo cung cấp làm dữ liệu thực hành Bài 5 (3D Cuboid).
Dữ liệu **không nằm trong repo**. Bạn tải riêng, giải nén vào thư mục này, và `.gitignore` chặn không cho commit.

## Tải và giải nén

Tải `Data-VF.zip` (khoảng 600 MB) **trước giờ học** từ link do coach phát:

(link GV gửi riêng)

Giải nén vào `data/` sao cho có `data/data-VF/sequence_01 … sequence_05`. Lệnh cho Windows và macOS ở [../docs/SETUP.md](../docs/SETUP.md) mục 4.
Để dữ liệu ở nơi khác (ổ D, USB) cũng được: ghi đường dẫn đầy đủ vào `data` trong [../configs/lab.ini](../configs/lab.ini).

## Cấu trúc

```text
data/data-VF/
└── sequence_01 … sequence_05/        5 sequence × 60 frame, cách nhau 1 giây
    ├── lidar/<timestamp>.bin         float32 × 4: x, y, z, intensity (không có trường ring)
    ├── cameras/camXX/<timestamp>.jpg cam01, 03, 05, 06, 07, 08, 09 · 1920×1020
    └── calib.json                    nội tham, méo ống kính, phép biến đổi camera ↔ LiDAR
```

| Mục | Nội dung |
|---|---|
| Cảm biến | 1 LiDAR 40 tia (LiDAR gốc 10 Hz, đã lấy mẫu 1 FPS), khoảng 63–68 nghìn điểm mỗi frame; 7 camera |
| Hệ tọa độ | Gốc ở tâm LiDAR trên nóc xe, mét. **x trái, y sau, z lên**; phía trước xe là −y; mặt đường khoảng z = −1,7 m. Xem [../docs/COORDINATES.md](../docs/COORDINATES.md) |
| Class | Car, Truck, Bus, Cyclist, Pedestrian |
| Mật độ vật | Trong 360°, ≤ 50 m: trung bình khoảng 18 vật mỗi frame (trung vị 17), khoảng 9 vật trong 30 m |

## 10 frame của bạn

Lệnh `python scripts/lab.py dry` chọn **10 frame cố định theo mã số**: mỗi sequence 2 frame, cách nhau ít nhất 15 frame (15 giây). Cùng mã số luôn ra cùng frame, trên mọi máy. Tên frame `s02f07` = sequence 02, frame chỉ số 7 (đếm từ 0). Các frame quá thưa vật không bao giờ được chọn.
Chỉ 10 frame này được đóng gói (khoảng 23 MB) và tải lên task CVAT của bạn. **Nhãn chuẩn không phát cho học viên.**

## Giấy phép và phạm vi dùng

- Dữ liệu **chỉ dùng trong lớp, trên máy của bạn và trong CVAT của lớp**. Không đăng lại, không chia sẻ ra ngoài.
- Ảnh camera có người và biển số thật: **không** dán ảnh hay ảnh chụp màn hình lên dịch vụ AI bên ngoài, nhóm chat, mạng xã hội.
- Repo của bạn là public: không commit bất cứ thứ gì trong `data/data-VF/`, `work/`, `submission/images/`.
- Hết khóa, xóa `data/data-VF/` trên máy.
