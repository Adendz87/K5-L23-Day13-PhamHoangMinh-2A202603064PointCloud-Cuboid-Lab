# SUBMISSION — nộp gì, nộp ở đâu

Hạn: **cuối buổi, 19:30**, trừ khi coach thông báo hạn khác trên LMS. Nộp lên LMS: https://aithucchien.vinuni.edu.vn

## Ba thứ bạn nộp

| Mã | Sản phẩm | Ở đâu | Coach kiểm bằng gì |
|---|---|---|---|
| E1 | Task CVAT `D13-<MÃ SỐ>` **đã Save** | Trên CVAT | Số cuboid và chất lượng cuboid, qua bảng A |
| E2 | `D13-<MÃ SỐ>-bangA.csv` | Thư mục nộp | Chấm tự động 40 điểm so với nhãn chuẩn. Phải khớp với task, không sửa tay |
| E3 | `<MÃ SỐ>-report.md` kèm ảnh chụp | Thư mục nộp | Chấm tay 60 điểm theo [RUBRIC.md](RUBRIC.md) |

Kèm theo: `D13-<MÃ SỐ>-tukiem.csv` (phiếu tự kiểm, không chấm điểm) và `prompts.md` (khai báo dùng AI).

## Cấu trúc thư mục nộp

```
K5-L23-DAY13-<HoVaTen>-<MSSV>-Cuboid/
├── D13-<MÃ SỐ>-bangA.csv        # E2 – từ lệnh report, chạy sau lần Save cuối
├── D13-<MÃ SỐ>-tukiem.csv       # từ lệnh check, chạy sau lần report cuối
├── <MÃ SỐ>-report.md            # E3 – theo templates/report.md
├── prompts.md                   # khai báo dùng AI
└── images/
    ├── t1-<frame>-3d.png        # T1: 2 frame đọc kỹ × (ảnh 3D + ảnh Top) = 4 ảnh
    ├── t1-<frame>-top.png       #     ảnh Top có đánh dấu phía trước, +x, +y
    ├── t2-a-car.png             # T2: ba cuboid mẫu = 3 ảnh
    ├── t2-b-bus-truck.png
    ├── t2-c-ped-cyclist.png
    ├── t4-1-bong-che.png        # T4: bốn hiện tượng = 4 ảnh
    ├── t4-2-thua-o-xa.png
    ├── t4-3-phan-xa-thap.png
    └── t4-4-diem-la.png
```

Tổng cộng 11 ảnh. Ảnh `.png` hoặc `.jpg` đều được. `<frame>` là tên frame, ví dụ `t1-s01f07-top.png`.

Nén cả thư mục thành `K5-L23-DAY13-<HoVaTen>-<MSSV>-Cuboid.zip` rồi nộp. `<HoVaTen>` viết liền, không dấu, ví dụ `K5-L23-DAY13-NguyenVanAn-2A202600123-Cuboid.zip`. Lệnh tạo thư mục và nén cho Windows và macOS ở [COMMANDS.md](COMMANDS.md) mục 7.

Nếu bạn làm trên **CVAT local**, coach không đọc được task trên máy bạn; bảng A chính là bài vẽ của bạn. Giữ nguyên CVAT (không `down -v`, không `--replace`) cho tới khi có điểm, phòng khi coach cần xem lại.

## Trước khi nộp — kiểm 6 điều

1. Đã **Save** job, rồi chạy `report`, rồi `check`, theo đúng thứ tự đó. Bảng A cũ hơn task thì coach chấm theo bảng A cũ.
2. Bảng A có **từ 50 cuboid**, frame 1 từ 8, mỗi frame còn lại từ 5.
3. Báo cáo điền đủ mục 2–5. Mọi con số có đơn vị (m, °).
4. Đủ 11 ảnh, tên đúng như trên, và báo cáo trỏ đúng tên ảnh.
5. `prompts.md` có mặt, kể cả khi ghi "Không dùng".
6. Trong zip **không có** `data-VF`, file `.bin`, `.pcd`, ảnh camera gốc, hay thư mục `xem/`. Chỉ ảnh chụp màn hình của báo cáo.

## Sau khi nộp

- Không sửa cuboid trong task sau hạn. Lỗi phát hiện thêm thì ghi vào mục 7 của báo cáo.
- Coach có thể phát cho bạn **phiếu hồ sơ lỗi** sau khi chốt bài nộp: số cuboid đúng, ngược hướng, sai class, vẽ lệch, bỏ sót, và độ phủ theo khoảng cách. Dùng phiếu này để chuẩn bị cho Ngày 24.
