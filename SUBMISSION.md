# Nộp bài

Bạn nộp **hai thứ** lên LMS **https://aithucchien.vinuni.edu.vn** (hoặc kênh giảng viên chỉ định):

1. **Link repo public** của bạn: có `submission/REPORT.md` và dòng tiêu đề README mang họ tên, MSHV.
2. **File zip** `work/K5-L23-DAY13-<MSHV>-nop.zip` do `python scripts/lab.py pack` tạo, gồm bảng A, phiếu tự kiểm và 11 ảnh chụp. Các file này **không** lên repo public, vì chúng lấy từ dữ liệu VF được cấp theo cam kết bảo mật.

## Repo
Một người **một repo public**. Tên repo: `K5-L23-DAY13-<MSHV>-PointCloudCuboid` (không dấu, nối bằng `-`). Theo hướng dẫn lớp nếu giảng viên đặt quy ước khác.

## Hạn
Nộp lần đầu lúc **19:30** (mốc CP7). Trong 20' dự phòng (19:40–20:00) bạn được sửa cuboid và nộp lại; **hạn cuối 20:00**: commit cuối trên GitHub và file zip cuối trên LMS trước giờ đó được chấm. Coach có thể thông báo hạn khác trên LMS.

## Trước khi nộp
1. Bấm **Save** trong CVAT, rồi `python scripts/lab.py sync` để bảng A và phiếu tự kiểm khớp task.
2. Đổi dòng tiêu đề `# Day 13 Lab ...` của `README.md` thành `# Day 13 Lab — <Họ và tên>: <MSHV> - <Họ và tên>` (thay cả dấu `<` `>`; MSHV phải trùng `student` trong `configs/lab.ini`).
3. Điền `submission/REPORT.md` (xoá mọi dấu TODO).
4. `python scripts/lab.py pack` (macOS: `make pack`): nén bảng A, phiếu tự kiểm và ảnh trong `submission/images/` thành `work/K5-L23-DAY13-<MSHV>-nop.zip`.
5. `python scripts/check_submission.py` (macOS: `make check`) hết **LỖI**. `CẢNH BÁO` thì đọc và tự quyết. Sửa gì sau bước này thì chạy lại `sync`, `pack` rồi `check_submission.py`.
6. Commit và push, mỗi lệnh một dòng (Windows và macOS như nhau; PowerShell 5.1 không chạy được `&&`):
   ```bash
   git add -A
   git commit -m "Day 13: bao cao"
   git push
   ```
7. Nộp lên LMS: **link repo** và **file zip** ở bước 4. Nộp lại trước 20:00 thì tải lên file zip mới nhất.

## Cấu trúc
```text
README.md                    # dòng tiêu đề có Họ và tên: MSHV - Họ và tên             -> repo
configs/lab.ini              # đã điền student, cvat_user (KHÔNG có mật khẩu)            -> repo
submission/
├── REPORT.md                # báo cáo duy nhất (6 mục)                                  -> repo
├── D13-<MSHV>-bangA.csv     # sinh bởi `python scripts/lab.py report`                   -> chỉ trong zip
├── D13-<MSHV>-tukiem.csv    # sinh bởi `python scripts/lab.py selfcheck`                -> chỉ trong zip
└── images/                  # 11 ảnh chụp                                               -> chỉ trong zip
    ├── t1-<frame>-3d.png    #   Bước 2 (T1): 2 frame đọc kỹ × (ảnh khung 3D + ảnh nhìn từ trên xuống) = 4 ảnh
    ├── t1-<frame>-top.png   #   ảnh nhìn từ trên xuống, có đánh dấu phía trước, +x, +y
    ├── t2-a-car.png         #   Bước 3 (T2): ba cuboid mẫu = 3 ảnh
    ├── t2-b-bus-truck.png
    ├── t2-c-ped-cyclist.png
    ├── t4-1-bong-che.png    #   Bước 4 (T4): bốn hiện tượng = 4 ảnh
    ├── t4-2-thua-o-xa.png
    ├── t4-3-phan-xa-thap.png
    └── t4-4-diem-la.png
```
`t1`, `t2`, `t4` là số nhiệm vụ T1–T5 của đề (Bước 2 = T1, Bước 3 = T2–T3, Bước 4 = T4). Ảnh `.png` hoặc `.jpg` đều được; `<frame>` là tên frame, ví dụ `t1-s01f21-top.png`. `.gitignore` chặn sẵn mọi file trong `submission/` trừ `REPORT.md`, nên `git add -A` không đưa bảng A hay ảnh lên repo.

## CVAT
Lớp không có máy chủ CVAT chung: task `D13-<MSHV>` nằm trên CVAT của máy bạn và coach không vào được. Coach chấm phần vẽ từ **bảng A** trong file zip; ảnh chụp trong CVAT (Bước 2–4) là bằng chứng bạn vẽ trên CVAT. Giữ nguyên CVAT (không `down -v`, không `--replace`) cho tới khi có điểm, phòng khi coach cần xem lại trên máy bạn.
