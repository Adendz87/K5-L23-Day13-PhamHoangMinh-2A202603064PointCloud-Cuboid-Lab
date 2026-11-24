# cvat_lab — công cụ Day 13 cho học viên

| File | Dùng để |
|---|---|
| `vf_cvat.py` | Lệnh bạn chạy: `day13`, `report`, `preview`, `check` |
| `vf_common.py` | Hàm dùng chung: chọn frame theo mã số, đọc point cloud, hình học cuboid |
| `vf_qa.py` | Chiếu cuboid lên ảnh camera và tự kiểm bằng point cloud |
| `requirements.txt` | `cvat-sdk`, `Pillow` |

Cần Python 3.10 trở lên. Cách cài ở [../SETUP.md](../SETUP.md); lệnh đầy đủ cho Windows và macOS ở [../COMMANDS.md](../COMMANDS.md). Chạy từ **thư mục gốc repo**:

```bash
python cvat_lab/vf_cvat.py day13 --student <MÃ SỐ> --data data-VF --dry-run
python cvat_lab/vf_cvat.py day13 --student <MÃ SỐ> --data data-VF --host <URL-CVAT> --user <tên> [--org <slug>]
python cvat_lab/vf_cvat.py report d13 --student <MÃ SỐ> --host <URL-CVAT> --user <tên> [--org <slug>] --out ./nop
python cvat_lab/vf_cvat.py preview d13 --student <MÃ SỐ> --data data-VF [--table nop/D13-<MÃ SỐ>-bangA.csv] [--out ./xem]
python cvat_lab/vf_cvat.py check d13 --student <MÃ SỐ> --data data-VF [--table nop/D13-<MÃ SỐ>-bangA.csv]
```

- Mỗi mã số được 10 frame cố định: 2 frame mỗi sequence, cách nhau ít nhất 15 frame. Tên frame có dạng `s02f07` (sequence 02, frame chỉ số 7, đếm từ 0). Frame quá thưa vật không bao giờ được chọn.
- Task có tên `D13-<MÃ SỐ>`, gồm một job 10 frame, mỗi frame có 7 ảnh camera đi kèm, và 5 label cuboid: Car, Truck, Bus, Cyclist, Pedestrian.
- Nếu task đã tồn tại, `day13` chỉ in link của task cũ. `--replace` **xóa task và mọi nhãn** rồi tạo lại.
- Mật khẩu được hỏi khi chạy, hoặc lấy từ biến môi trường `CVAT_PASSWORD`. Không bao giờ ghi mật khẩu vào file.
- `preview` và `check` chỉ đọc `calib.json`, ảnh và point cloud bạn đã có cùng bảng A của bạn. Chúng không dùng nhãn chuẩn và không tính điểm.

Đừng sửa các file `.py` trong thư mục này. Coach chấm bằng cùng bộ quy ước; bản sửa của bạn có thể cho ra bảng A sai.
