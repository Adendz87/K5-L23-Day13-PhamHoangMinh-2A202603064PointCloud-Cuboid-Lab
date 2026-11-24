# Nộp bài

## Repo
Một người **một repo public**. Tên repo: `K5-L23-DAY13-<MSHV>-PointCloudCuboid` (không dấu, nối bằng `-`). Theo hướng dẫn lớp nếu giảng viên đặt quy ước khác.

Hạn: **cuối buổi, 19:30**, trừ khi coach thông báo hạn khác trên LMS.

## Trước khi nộp
1. Bấm **Save** trong CVAT, rồi `python scripts/lab.py sync` để bảng A và phiếu tự kiểm khớp task.
2. Đổi dòng tiêu đề `# Day 13 Lab ...` của `README.md`: `# Day 13 Lab — <Họ và tên>: <MSHV> - <Họ và tên>`.
3. Điền `submission/REPORT.md` (xoá mọi dòng `TODO(học viên)`).
4. `python scripts/check_submission.py` (macOS: `make check`) hết **LỖI**. `CẢNH BÁO` thì đọc và tự quyết.
5. `python scripts/lab.py pack` (macOS: `make pack`) nén ảnh chụp thành `work/K5-L23-DAY13-<MÃ SỐ>-images.zip`.
6. `git add -A && git commit && git push`.
7. Nộp lên LMS **https://aithucchien.vinuni.edu.vn** hoặc kênh giảng viên chỉ định: **link repo** và **file zip ảnh**.

## Cấu trúc bắt buộc
```text
README.md                              # dòng tiêu đề có MSHV - Họ và tên
configs/lab.ini                        # đã điền student, cvat_user (KHÔNG có mật khẩu)
submission/
├── REPORT.md                          # báo cáo duy nhất (6 mục)
├── D13-<MÃ SỐ>-bangA.csv              # sinh bởi `python scripts/lab.py report`
├── D13-<MÃ SỐ>-tukiem.csv             # sinh bởi `python scripts/lab.py selfcheck`
└── images/                            # 11 ảnh chụp: CHỈ nộp qua LMS, git không theo dõi
    ├── t1-<frame>-3d.png              #   Bước 2: 2 frame đọc kỹ × (ảnh 3D + ảnh Top) = 4 ảnh
    ├── t1-<frame>-top.png             #   ảnh Top có đánh dấu phía trước, +x, +y
    ├── t2-a-car.png                   #   Bước 3: ba cuboid mẫu = 3 ảnh
    ├── t2-b-bus-truck.png
    ├── t2-c-ped-cyclist.png
    ├── t4-1-bong-che.png              #   Bước 4: bốn hiện tượng = 4 ảnh
    ├── t4-2-thua-o-xa.png
    ├── t4-3-phan-xa-thap.png
    └── t4-4-diem-la.png
```
Không commit `work/`, `data/data-VF/`, ảnh, file `.bin`, `.pcd`, `.zip`. Ảnh `.png` hoặc `.jpg` đều được; `<frame>` là tên frame, ví dụ `t1-s01f07-top.png`.

## Task CVAT
Task `D13-<MÃ SỐ>` đã Save cũng là một phần bài nộp. Nếu bạn làm trên **CVAT local**, coach không đọc được task trên máy bạn và chấm bằng bảng A trong repo. Giữ nguyên CVAT (không `down -v`, không `--replace`) cho tới khi có điểm, phòng khi coach cần xem lại.
