# Nộp bài

## Repo
Một người **một repo public**. Tên repo: `K5-L23-DAY13-<MSHV>-PointCloudCuboid` (không dấu, nối bằng `-`). Theo hướng dẫn lớp nếu giảng viên đặt quy ước khác.

Nộp lần đầu lúc **19:30** (mốc CP7). Trong 20' dự phòng bạn được sửa và push lại; **hạn cuối 20:00**, bản push cuối cùng trước giờ đó được chấm. Coach có thể thông báo hạn khác trên LMS.

## Trước khi nộp
1. Bấm **Save** trong CVAT, rồi `python scripts/lab.py sync` để bảng A và phiếu tự kiểm khớp task.
2. Đổi dòng tiêu đề `# Day 13 Lab ...` của `README.md`: `# Day 13 Lab — <Họ và tên>: <MSHV> - <Họ và tên>`.
3. Điền `submission/REPORT.md` (xoá mọi dòng `TODO(học viên)`).
4. `python scripts/check_submission.py` (macOS: `make check`) hết **LỖI**. `CẢNH BÁO` thì đọc và tự quyết.
5. `python scripts/lab.py pack` (macOS: `make pack`) nén ảnh chụp thành `work/K5-L23-DAY13-<MÃ SỐ>-images.zip`.
6. Commit và push, mỗi lệnh một dòng (Windows và macOS như nhau; PowerShell 5.1 không chạy được `&&`):
   ```bash
   git add -A
   git commit -m "Day 13: bang A, phieu tu kiem, bao cao"
   git push
   ```
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
Lớp không có máy chủ CVAT chung: task `D13-<MÃ SỐ>` nằm trên CVAT local của máy bạn và coach không vào được. Coach chấm phần vẽ từ **bảng A** trong repo; ảnh chụp trong CVAT (Bước 2–4) là bằng chứng bạn vẽ trên CVAT. Giữ nguyên CVAT (không `down -v`, không `--replace`) cho tới khi có điểm, phòng khi coach cần xem lại trên máy bạn.
