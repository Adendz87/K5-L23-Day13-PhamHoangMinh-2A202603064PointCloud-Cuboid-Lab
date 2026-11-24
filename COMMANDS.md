# COMMANDS — mọi lệnh của buổi lab, Windows và macOS

Mọi lệnh chạy **từ thư mục gốc của repo** (thư mục chứa `README.md` và `cvat_lab/`), sau khi đã kích hoạt môi trường `.venv`. Đầu dòng lệnh phải có chữ `(.venv)`.

Thay các chỗ `<...>` bằng giá trị của bạn, bỏ luôn dấu `<` `>`:

| Chỗ thay | Ý nghĩa | Ví dụ |
|---|---|---|
| `<MÃ SỐ>` | Mã số học viên của bạn, trừ khi coach giao mã khác. Chỉ gồm chữ, số, `-`, `_` | `2A202600123` |
| `<tên>` | Tên đăng nhập CVAT của bạn | `an.nguyen` |
| `http://localhost:8080` | Địa chỉ CVAT. Đổi thành địa chỉ coach phát nếu lớp dùng máy chủ chung | |
| `data-VF` | Thư mục dữ liệu. Đổi thành đường dẫn đầy đủ trong nháy kép nếu để nơi khác | `"D:\lab\Data-VF"` |

Lệnh nào nối tới CVAT sẽ hỏi `Mật khẩu CVAT cho <tên>:`. Gõ mật khẩu rồi Enter; màn hình không hiện ký tự nào.

## 0. Mỗi lần mở terminal mới

**Windows (PowerShell)**

```powershell
cd $HOME\Documents\K5-L23-Day13-PointCloud-Cuboid-Student
.\.venv\Scripts\Activate.ps1
```

**macOS (Terminal)**

```bash
cd ~/Documents/K5-L23-Day13-PointCloud-Cuboid-Student
source .venv/bin/activate
```

Bật CVAT local nếu đang tắt (chạy trong thư mục `cvat`, giống nhau trên hai hệ điều hành):

```bash
docker compose up -d
```

## 1. P0 · Xem 10 frame của bạn (không nối CVAT)

Giống nhau trên Windows và macOS:

```bash
python cvat_lab/vf_cvat.py day13 --student <MÃ SỐ> --data data-VF --dry-run
```

## 2. P0 · Tạo task `D13-<MÃ SỐ>` trên CVAT

Giống nhau trên Windows và macOS:

```bash
python cvat_lab/vf_cvat.py day13 --student <MÃ SỐ> --data data-VF --host http://localhost:8080 --user <tên>
```

Lệnh in đường dẫn task, dạng `http://localhost:8080/tasks/12`. Mở đường dẫn bằng Chrome hoặc Edge:

**Windows (PowerShell)**

```powershell
Start-Process "http://localhost:8080/tasks"
```

**macOS (Terminal)**

```bash
open "http://localhost:8080/tasks"
```

Nếu coach yêu cầu tạo task trong tổ chức CVAT của lớp, thêm `--org <slug>` (coach phát slug) vào lệnh này **và** lệnh `report`:

```bash
python cvat_lab/vf_cvat.py day13 --student <MÃ SỐ> --data data-VF --host <URL-CVAT> --user <tên> --org <slug>
```

Chạy lại lệnh khi task đã có chỉ in lại đường dẫn task cũ, không tạo thêm. **Không thêm `--replace` nếu bạn đã vẽ gì**: `--replace` xóa task cùng mọi cuboid rồi tạo lại.

## 3. T5 · Xuất bảng A từ cuboid của bạn

Bấm **Save** trong CVAT trước. Giống nhau trên Windows và macOS:

```bash
python cvat_lab/vf_cvat.py report d13 --student <MÃ SỐ> --host http://localhost:8080 --user <tên> --out ./nop
```

Kết quả là `nop/D13-<MÃ SỐ>-bangA.csv`, kèm số cuboid của từng frame in ra màn hình. Mở file bằng bảng tính:

**Windows (PowerShell)**

```powershell
Invoke-Item nop\D13-<MÃ SỐ>-bangA.csv
```

**macOS (Terminal)**

```bash
open nop/D13-<MÃ SỐ>-bangA.csv
```

Mỗi lần sửa cuboid trên CVAT: Save, rồi chạy lại `report` để bảng A cập nhật.

## 4. Tự kiểm · Vẽ cuboid của bạn lên ảnh camera (`preview`)

Cần bảng A ở bước 3. Giống nhau trên Windows và macOS:

```bash
python cvat_lab/vf_cvat.py preview d13 --student <MÃ SỐ> --data data-VF
```

Mỗi frame ra một ảnh trong `xem/`, gồm 7 ảnh camera và một ảnh nhìn từ trên xuống, có cuboid của bạn vẽ đè. Mở thư mục ảnh:

**Windows (PowerShell)**

```powershell
Invoke-Item xem
```

**macOS (Terminal)**

```bash
open xem
```

## 5. Tự kiểm · Soát cuboid bằng point cloud (`check`)

Cần bảng A ở bước 3. Giống nhau trên Windows và macOS:

```bash
python cvat_lab/vf_cvat.py check d13 --student <MÃ SỐ> --data data-VF
```

Kết quả là `nop/D13-<MÃ SỐ>-tukiem.csv`, và danh sách cuboid có cảnh báo in ra màn hình. Cảnh báo là **gợi ý để xem lại**, không phải lỗi chắc chắn và không tính điểm (xem [CHECKPOINTS.md](CHECKPOINTS.md)).

## 6. Mật khẩu qua biến môi trường (không bắt buộc)

Nếu không muốn gõ mật khẩu mỗi lần, đặt biến `CVAT_PASSWORD` cho **cửa sổ terminal đang mở**. Không ghi mật khẩu vào file nào.

**Windows (PowerShell)**

```powershell
$env:CVAT_PASSWORD = [Net.NetworkCredential]::new('', (Read-Host "Mat khau CVAT" -AsSecureString)).Password
```

Xóa khi xong:

```powershell
Remove-Item Env:CVAT_PASSWORD
```

**macOS (Terminal)**

```bash
read -s "CVAT_PASSWORD?Mat khau CVAT: " && export CVAT_PASSWORD
```

Xóa khi xong:

```bash
unset CVAT_PASSWORD
```

## 7. Đóng gói bài nộp

Tạo thư mục nộp và chép file theo [SUBMISSION.md](SUBMISSION.md). Thay `<HoVaTen>`, `<MSSV>`, `<MÃ SỐ>`.

**Windows (PowerShell)**

```powershell
$nop = "K5-L23-DAY13-<HoVaTen>-<MSSV>-Cuboid"
New-Item -ItemType Directory -Force "$nop\images"
Copy-Item nop\D13-<MÃ SỐ>-bangA.csv, nop\D13-<MÃ SỐ>-tukiem.csv $nop
Copy-Item templates\report.md "$nop\<MÃ SỐ>-report.md"
Copy-Item templates\prompts.md $nop
```

Sau khi điền báo cáo và chép ảnh chụp vào `images\`:

```powershell
Compress-Archive -Path $nop -DestinationPath "$nop.zip" -Force
```

**macOS (Terminal)**

```bash
nop="K5-L23-DAY13-<HoVaTen>-<MSSV>-Cuboid"
mkdir -p "$nop/images"
cp nop/D13-<MÃ SỐ>-bangA.csv nop/D13-<MÃ SỐ>-tukiem.csv "$nop/"
cp templates/report.md "$nop/<MÃ SỐ>-report.md"
cp templates/prompts.md "$nop/"
```

Sau khi điền báo cáo và chép ảnh chụp vào `images/`:

```bash
zip -r "$nop.zip" "$nop" -x "*.DS_Store"
```

Chép `report.md` **một lần** ở đầu buổi rồi điền dần. Chạy lại lệnh `Copy-Item` / `cp` sẽ ghi đè báo cáo đang viết.

## 8. Chụp màn hình

| | Chụp một vùng | Ảnh lưu ở đâu |
|---|---|---|
| Windows | `Win + Shift + S`, kéo chọn vùng | Bấm vào thông báo để lưu, hoặc dán vào Paint rồi lưu PNG |
| macOS | `Cmd + Shift + 4`, kéo chọn vùng | Desktop |

Đặt tên ảnh theo [SUBMISSION.md](SUBMISSION.md) và chép vào thư mục `images` của bài nộp.

## 9. Xem trợ giúp của lệnh

```bash
python cvat_lab/vf_cvat.py --help
```

```bash
python cvat_lab/vf_cvat.py day13 --help
```
