# Cài đặt môi trường (làm trước buổi học)

Mục tiêu: trước 16:00 Ngày 13, máy bạn chạy được lệnh `--dry-run` ở mục 5 và mở được CVAT. Tổng thời gian khoảng 30–60 phút, phần lớn là chờ tải. Nếu kẹt, báo coach **trước buổi học**.

Mỗi bước có hai khối lệnh. Chọn đúng khối của máy bạn:

- **Windows**: mở **PowerShell** (bấm Start, gõ `powershell`). Không dùng Command Prompt (cmd).
- **macOS**: mở **Terminal** (Cmd + Space, gõ `terminal`).

Chỗ nào có `<...>` là chỗ bạn thay bằng giá trị của mình, bỏ luôn dấu `<` `>`.

## 1. Kiểm công cụ đã có chưa

**Windows (PowerShell)**

```powershell
git --version
python --version
docker --version
```

**macOS (Terminal)**

```bash
git --version
python3 --version
docker --version
```

Cần `git` bất kỳ bản nào và Python **3.11 trở lên** (khuyên dùng 3.12). `cvat-sdk` từ bản 2.80 (bản mới nhất là 2.83) và Pillow 13 không còn hỗ trợ Python 3.10, nên với Python cũ hơn 3.11, bước cài thư viện ở mục 3 sẽ báo lỗi. `docker` chỉ cần nếu bạn cài CVAT trên máy ([CVAT_SETUP.md](CVAT_SETUP.md)). Thiếu cái nào thì cài ở mục 2; đủ rồi thì sang mục 3.

Trên Windows, nếu `python --version` mở Microsoft Store hoặc không in gì, coi như chưa có Python. Trên macOS, `python3` có sẵn của Apple là bản 3.9: không dùng được, cài bản mới ở mục 2.

## 2. Cài công cụ còn thiếu

**Windows (PowerShell)**

```powershell
winget install -e --id Git.Git
winget install -e --id Python.Python.3.12
winget install -e --id Docker.DockerDesktop
```

Cài xong, **đóng PowerShell và mở lại** để nhận lệnh mới. Nếu máy không có `winget`, tải bộ cài từ https://git-scm.com, https://www.python.org/downloads/ (chọn bản 3.12, tick **Add python.exe to PATH**) và https://www.docker.com/products/docker-desktop/.

Nếu máy đã có sẵn một Python cũ hơn 3.11, `python --version` có thể vẫn in bản cũ sau khi cài. Khi đó dùng `py -3.12` thay cho `python` ở dòng tạo `.venv` (mục 3).

Docker Desktop trên Windows cần WSL 2. Nếu Docker báo thiếu, chạy lệnh sau trong PowerShell mở bằng **Run as administrator**, rồi khởi động lại máy:

```powershell
wsl --install
```

**macOS (Terminal)**

Cài Homebrew nếu chưa có (kiểm bằng `brew --version`), theo hướng dẫn tại https://brew.sh. Sau đó:

```bash
brew install git python@3.12
brew install --cask docker
```

Lần đầu gõ `git` trên macOS có thể hiện hộp thoại cài Command Line Tools. Bấm **Install** và chờ xong.

Homebrew cài Python 3.12 dưới tên lệnh `python3.12`; lệnh `python3` có thể vẫn trỏ vào bản 3.9 của Apple. Kiểm bằng `python3.12 --version`, và dùng `python3.12` ở dòng tạo `.venv` (mục 3).

## 3. Tạo repo của bạn, tải về và cài thư viện

Trên GitHub, mở https://github.com/VinUni-AI20k/K5-L23-Day13-PointCloud-Cuboid-Lab, bấm **Use this template → Create a new repository**, chọn **Public**, đặt tên `K5-L23-DAY13-<MSHV>-PointCloudCuboid` (xem [../SUBMISSION.md](../SUBMISSION.md)). Trong các lệnh dưới, thay `<tài-khoản>` bằng tên tài khoản GitHub và `<MSHV>` bằng mã số của bạn.

**Windows (PowerShell)**

```powershell
cd $HOME\Documents
git clone https://github.com/<tài-khoản>/K5-L23-DAY13-<MSHV>-PointCloudCuboid.git
cd K5-L23-DAY13-<MSHV>-PointCloudCuboid
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Nếu `python --version` ở mục 1 in bản dưới 3.11, thay dòng `python -m venv .venv` bằng:

```powershell
py -3.12 -m venv .venv
```

Nếu dòng `Activate.ps1` báo *running scripts is disabled on this system*, chạy lệnh sau rồi kích hoạt lại. Lệnh chỉ có hiệu lực trong cửa sổ PowerShell đang mở:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**macOS (Terminal)**

```bash
cd ~/Documents
git clone https://github.com/<tài-khoản>/K5-L23-DAY13-<MSHV>-PointCloudCuboid.git
cd K5-L23-DAY13-<MSHV>-PointCloudCuboid
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Nếu `python3 --version` ở mục 1 in bản dưới 3.11 (ví dụ bản 3.9 có sẵn của macOS), thay dòng `python3 -m venv .venv` bằng:

```bash
python3.12 -m venv .venv
```

Kích hoạt thành công thì đầu dòng lệnh có chữ `(.venv)`. Từ đây lệnh `python` giống nhau trên cả hai hệ điều hành. Kiểm lại bằng `python --version`: phải in **3.11 trở lên**. Nếu không, `.venv` đã được tạo bằng Python cũ: xoá và tạo lại theo [COMMON_ERRORS.md](COMMON_ERRORS.md) mục 1. Thư viện rất nhẹ (`cvat-sdk`, `Pillow`), không cần GPU.

**Mỗi lần mở cửa sổ terminal mới**, bạn phải vào lại thư mục repo và kích hoạt lại môi trường ([COMMANDS.md](COMMANDS.md) mục 0).

## 4. Tải và giải nén dữ liệu VF

Tải `Data-VF.zip` (khoảng 600 MB) bằng trình duyệt từ link GV gửi riêng cho bạn (xem [../data/README.md](../data/README.md)). Tải **trước giờ học**. Các lệnh dưới giả định file nằm trong thư mục Downloads và bạn đang đứng trong thư mục repo.

**Windows (PowerShell)**

```powershell
tar -xf "$HOME\Downloads\Data-VF.zip" -C data
Get-ChildItem data\data-VF
```

**macOS (Terminal)**

```bash
unzip -q ~/Downloads/Data-VF.zip -d data
ls data/data-VF
```

Lệnh thứ hai phải liệt kê `sequence_01` đến `sequence_05`. Thư mục có thể mang tên `Data-VF` hoặc `data-VF`; Windows và macOS không phân biệt hoa thường nên lệnh vẫn chạy.

Nếu giải nén ra thẳng các thư mục `sequence_XX` trong `data/` (không có thư mục bọc ngoài), tạo `data/data-VF` rồi chuyển chúng vào:

```powershell
New-Item -ItemType Directory -Force data\data-VF
Move-Item data\sequence_* data\data-VF
```

```bash
mkdir -p data/data-VF && mv data/sequence_* data/data-VF/
```

Nếu bạn để dữ liệu ở nơi khác (ổ D, USB), không cần chép lại: ghi đường dẫn đầy đủ vào dòng `data =` trong `configs/lab.ini`, ví dụ `data = D:\lab\Data-VF` hoặc `data = /Volumes/USB/Data-VF`.

## 5. Điền cấu hình và chạy thử (không cần CVAT)

Mở `configs/lab.ini` và điền `student` (mã số học viên của bạn). **Không ghi mật khẩu vào file này.**

**Windows (PowerShell)**

```powershell
notepad configs\lab.ini
```

**macOS (Terminal)**

```bash
open -e configs/lab.ini
```

Lưu file, rồi chạy (giống nhau trên hai hệ điều hành):

```bash
python scripts/lab.py dry
```

Kết quả đúng có dạng:

```
Task: D13-2A202600123
10 frame của bạn (chỉ số đếm từ 0):
  s01f07  sequence_01  ts=...  camera=7
  ...
Đã đóng gói 23.1 MB trong 2.4 s.
--dry-run: không kết nối CVAT.
```

Kiểm ba điều: có đủ 10 dòng frame, mỗi dòng `camera=7`, và dòng cuối báo `--dry-run`. Chạy lại cùng mã số luôn ra cùng 10 frame.

## 6. Cài CVAT

Làm theo [CVAT_SETUP.md](CVAT_SETUP.md), rồi điền `cvat_user` trong `configs/lab.ini`. Nếu coach thông báo lớp dùng máy chủ CVAT chung, bạn bỏ qua bước cài: đổi `cvat_host` thành địa chỉ coach phát và mở thử địa chỉ đó bằng Chrome hoặc Edge.

## Bảng kiểm trước buổi học

- [ ] `python --version` (đã kích hoạt `.venv`) in 3.11 trở lên.
- [ ] `python scripts/lab.py dry` in đủ 10 frame, mỗi frame 7 camera.
- [ ] Mở được CVAT và đăng nhập được.
- [ ] Đã đọc [COORDINATES.md](COORDINATES.md), [GUIDELINE.md](GUIDELINE.md) và [../RULES.md](../RULES.md).
