# SETUP — chuẩn bị máy (làm trước buổi học)

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

Cần `git` bất kỳ bản nào, Python **3.10 trở lên**. `docker` chỉ cần nếu bạn cài CVAT trên máy ([INSTALL_CVAT.md](INSTALL_CVAT.md)). Thiếu cái nào thì cài ở mục 2; đủ rồi thì sang mục 3.

Trên Windows, nếu `python --version` mở Microsoft Store hoặc không in gì, coi như chưa có Python.

## 2. Cài công cụ còn thiếu

**Windows (PowerShell)**

```powershell
winget install -e --id Git.Git
winget install -e --id Python.Python.3.12
winget install -e --id Docker.DockerDesktop
```

Cài xong, **đóng PowerShell và mở lại** để nhận lệnh mới. Nếu máy không có `winget`, tải bộ cài từ https://git-scm.com, https://www.python.org/downloads/ (tick **Add python.exe to PATH**) và https://www.docker.com/products/docker-desktop/.

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

## 3. Tải repo và cài thư viện

**Windows (PowerShell)**

```powershell
cd $HOME\Documents
git clone https://github.com/VinUni-AI20k/K5-L23-Day13-PointCloud-Cuboid-Student.git
cd K5-L23-Day13-PointCloud-Cuboid-Student
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r cvat_lab/requirements.txt
```

Nếu dòng `Activate.ps1` báo *running scripts is disabled on this system*, chạy lệnh sau rồi kích hoạt lại. Lệnh chỉ có hiệu lực trong cửa sổ PowerShell đang mở:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**macOS (Terminal)**

```bash
cd ~/Documents
git clone https://github.com/VinUni-AI20k/K5-L23-Day13-PointCloud-Cuboid-Student.git
cd K5-L23-Day13-PointCloud-Cuboid-Student
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r cvat_lab/requirements.txt
```

Kích hoạt thành công thì đầu dòng lệnh có chữ `(.venv)`. Từ đây lệnh `python` giống nhau trên cả hai hệ điều hành.

Không dùng Git cũng được: trên trang GitHub của repo bấm **Code → Download ZIP**, giải nén, rồi `cd` vào thư mục vừa giải nén và chạy từ dòng `python -m venv` trở đi.

**Mỗi lần mở cửa sổ terminal mới**, bạn phải vào lại thư mục repo và kích hoạt lại môi trường:

```powershell
cd $HOME\Documents\K5-L23-Day13-PointCloud-Cuboid-Student
.\.venv\Scripts\Activate.ps1
```

```bash
cd ~/Documents/K5-L23-Day13-PointCloud-Cuboid-Student
source .venv/bin/activate
```

## 4. Tải và giải nén dữ liệu VF

Tải `Data-VF.zip` (khoảng 600 MB) bằng trình duyệt từ link do coach phát:

(link GV gửi riêng)

Tải **trước giờ học**. Các lệnh dưới giả định file nằm trong thư mục Downloads và bạn đang đứng trong thư mục repo.

**Windows (PowerShell)**

```powershell
tar -xf "$HOME\Downloads\Data-VF.zip"
Get-ChildItem data-VF
```

**macOS (Terminal)**

```bash
unzip -q ~/Downloads/Data-VF.zip -d .
ls data-VF
```

Lệnh thứ hai phải liệt kê `sequence_01` đến `sequence_05`. Thư mục có thể mang tên `Data-VF` hoặc `data-VF`; Windows và macOS không phân biệt hoa thường nên lệnh vẫn chạy.

Nếu giải nén ra thẳng các thư mục `sequence_XX` (không có thư mục bọc ngoài), tạo thư mục `data-VF` rồi chuyển chúng vào:

```powershell
New-Item -ItemType Directory -Force data-VF
Move-Item sequence_* data-VF
```

```bash
mkdir -p data-VF && mv sequence_* data-VF/
```

Nếu bạn để dữ liệu ở nơi khác (ổ D, USB), không cần chép lại: thay `data-VF` trong mọi lệnh bằng đường dẫn đầy đủ, đặt trong dấu nháy kép, ví dụ `--data "D:\lab\Data-VF"` hoặc `--data "/Volumes/USB/Data-VF"`.

## 5. Chạy thử (không cần CVAT)

Giống nhau trên Windows và macOS. Thay `<MÃ SỐ>` bằng mã số học viên của bạn:

```bash
python cvat_lab/vf_cvat.py day13 --student <MÃ SỐ> --data data-VF --dry-run
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

Làm theo [INSTALL_CVAT.md](INSTALL_CVAT.md). Nếu coach thông báo lớp dùng máy chủ CVAT chung, bạn bỏ qua bước cài và chỉ cần mở được địa chỉ coach phát bằng Chrome hoặc Edge.

## Bảng kiểm trước buổi học

- [ ] `python --version` (đã kích hoạt `.venv`) in 3.10 trở lên.
- [ ] Lệnh `--dry-run` in đủ 10 frame, mỗi frame 7 camera.
- [ ] Mở được CVAT và đăng nhập được.
- [ ] Đã đọc [GUIDE.md](GUIDE.md) mục 1–3 và [RULES.md](RULES.md).
