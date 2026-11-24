# Lab Ngày 13 — Đọc point cloud VF và vẽ cuboid đầu tiên trên CVAT 3D

AI20K K5 · L2–L3 · Ngày 13 · Buổi thực hành 16:00–20:00 · làm **cá nhân**, ngồi theo cặp để đổi kiểm

Mỗi bạn có một task CVAT riêng gồm **10 frame LiDAR thật** của dữ liệu VF (1 LiDAR 40 tia + 7 camera), chọn cố định theo mã số của bạn. Bạn đọc frame, đổi giữa các view 3D / Top / Side / Front, vẽ cuboid cho các vật quanh xe (360°, xa ≤ 50 m, ưu tiên vật gần) theo guideline 3D Cuboid, săn bốn hiện tượng làm hỏng point cloud, rồi đọc lại số đo từ chính cuboid của mình.

Cuboid hôm nay là hình đơn lẻ trên từng frame, **không phải track**. Track, nội suy và khóa kích thước là nội dung Ngày 24–26.

## Đọc theo thứ tự

| Khi nào | File | Nội dung |
|---|---|---|
| **Trước buổi học** | [SETUP.md](SETUP.md) | Cài Git, Python, tải repo và dữ liệu, chạy thử. Lệnh cho Windows và macOS |
| **Trước buổi học** | [INSTALL_CVAT.md](INSTALL_CVAT.md) | Cài CVAT trên máy, tạo tài khoản, mở `localhost:8080` |
| Trước buổi học | [GUIDE.md](GUIDE.md) | Hệ tọa độ VF, tóm tắt guideline, đề bài P0–T5 |
| Đầu buổi | [RULES.md](RULES.md) | Làm cá nhân, giữ dữ liệu trong lớp, dùng AI |
| Trong buổi | [COMMANDS.md](COMMANDS.md) | **Mọi lệnh của buổi lab**, Windows và macOS cạnh nhau |
| Trong buổi | [CHECKPOINTS.md](CHECKPOINTS.md) | Các mốc tự kiểm: `report`, `preview`, `check` |
| Khi kẹt | [COMMON_ERRORS.md](COMMON_ERRORS.md) | Lỗi hay gặp và cách tự gỡ |
| Trước khi nộp | [SUBMISSION.md](SUBMISSION.md), [RUBRIC.md](RUBRIC.md) | Nộp gì, chấm thế nào |
| Mẫu điền | [templates/](templates/) | `report.md`, `prompts.md` |
| Tài liệu gốc | [guideline/3D_Cuboid_Annotation_Guideline.docx](guideline/3D_Cuboid_Annotation_Guideline.docx) | Guideline 3D Cuboid đầy đủ, có hình minh họa |

## Bắt đầu nhanh

Chi tiết từng bước ở [SETUP.md](SETUP.md). Nếu máy đã có Git, Python 3.10+ và CVAT đang chạy:

**Windows (PowerShell)**

```powershell
git clone https://github.com/VinUni-AI20k/K5-L23-Day13-PointCloud-Cuboid-Student.git
cd K5-L23-Day13-PointCloud-Cuboid-Student
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r cvat_lab/requirements.txt
python cvat_lab/vf_cvat.py day13 --student <MÃ SỐ> --data data-VF --dry-run
```

**macOS (Terminal)**

```bash
git clone https://github.com/VinUni-AI20k/K5-L23-Day13-PointCloud-Cuboid-Student.git
cd K5-L23-Day13-PointCloud-Cuboid-Student
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r cvat_lab/requirements.txt
python cvat_lab/vf_cvat.py day13 --student <MÃ SỐ> --data data-VF --dry-run
```

Lệnh cuối in ra tên 10 frame của bạn và không kết nối CVAT. Thấy 10 dòng `sXXfYY` là máy đã sẵn sàng.

## Bạn nhận được gì

```
K5-L23-Day13-PointCloud-Cuboid-Student/
  cvat_lab/        vf_cvat.py (lệnh bạn chạy), vf_common.py, vf_qa.py, requirements.txt
  cvat-local/      docker-compose.lowspec.yml cho máy yếu
  guideline/       3D_Cuboid_Annotation_Guideline.docx
  templates/       report.md (mẫu báo cáo), prompts.md (khai báo dùng AI)
  data-VF/         dữ liệu bạn tự tải và giải nén vào đây (git không theo dõi)
  nop/             bảng A và phiếu tự kiểm do lệnh sinh ra (git không theo dõi)
  xem/             ảnh xem trước do lệnh preview sinh ra (git không theo dõi)
```

Dữ liệu `data-VF` (khoảng 600 MB khi nén) tải riêng, xem [SETUP.md](SETUP.md) mục 4:

```
data-VF/
  sequence_01 … sequence_05/
    lidar/*.bin              float32 × 4: x, y, z, intensity
    cameras/camXX/*.jpg      cam01, 03, 05, 06, 07, 08, 09 (1920×1020)
    calib.json
```

## Cần có trên máy

- **Python 3.10 trở lên** và **Git**.
- **CVAT 3D** theo [INSTALL_CVAT.md](INSTALL_CVAT.md) (bản lớp dùng: **v2.83.0**), hoặc địa chỉ máy chủ CVAT do coach phát.
- **Chrome hoặc Edge.** CVAT chỉ hỗ trợ trình duyệt nhân Chromium.
- Khoảng 2 GB đĩa trống cho dữ liệu, thêm khoảng 10 GB nếu cài CVAT local.
- Chuột có nút giữa (con lăn). Vẽ cuboid 3D bằng touchpad rất chậm.

## Hệ tọa độ VF (nhớ trước khi vẽ)

Gốc ở tâm LiDAR trên nóc xe, đơn vị mét. **x sang trái, y ra sau, z lên.** Phía trước xe là **−y**, bên phải là −x, mặt đường khoảng z = −1,7 m. Yaw đo từ +x, ngược chiều kim đồng hồ nhìn từ trên: xe cùng chiều phía trước có yaw ≈ 270°, xe ngược chiều ≈ 90°.

## Dữ liệu và giấy phép

- **Dữ liệu VF**: dữ liệu lái xe thực tế của dự án, do ban đào tạo cung cấp làm dữ liệu thực hành. 5 sequence × 60 frame, cách nhau 1 giây.
- Dữ liệu **chỉ dùng trong lớp, trên máy của bạn**. Không đăng lại, không commit vào Git, không đưa lên dịch vụ ngoài, không gửi vào nhóm chat (xem [RULES.md](RULES.md)).
