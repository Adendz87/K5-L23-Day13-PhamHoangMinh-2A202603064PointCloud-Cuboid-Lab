# Cài CVAT trên máy cá nhân (làm trước buổi học)

Mục tiêu: máy bạn mở được `http://localhost:8080` và đăng nhập được CVAT. Cài lần đầu mất khoảng 20–40 phút, phần lớn là tải khoảng 5,8 GB image Docker. **Không cài trong giờ học.**

Phiên bản lớp dùng: **CVAT v2.83.0**. Nếu máy bạn còn CVAT từ Ngày 12 (v2.82.0) đang chạy tốt, bạn dùng tiếp được, không cần cài lại; các lệnh `task`, `report` sẽ in cảnh báo phiên bản, bỏ qua được (mục 8).

Lớp **không có máy chủ CVAT chung**: mỗi người chạy CVAT trên máy mình, task và nhãn chỉ nằm trên máy đó. Coach không vào được máy bạn; phần vẽ được chấm từ bảng A bạn nộp.

Nguồn: https://docs.cvat.ai/docs/administration/basics/installation/

## 1. Cần có

- **Docker Desktop** đã cài ([SETUP.md](SETUP.md) mục 2) và **đang mở**, biểu tượng cá voi báo *Engine running*.
- **Git**, **Chrome hoặc Edge**, ít nhất 10 GB đĩa trống (15 GB nếu sau này cập nhật CVAT).
- RAM cho Docker: khoảng 8 GB nếu máy có 16 GB. Máy 8 GB xem mục 6.
- **Mac chip Apple (M1 trở lên):** Docker Desktop → Settings → General → bật **Use Rosetta for x86_64/amd64 emulation on Apple Silicon**. Image `cvat/server` chỉ có bản amd64.

Kiểm Docker đã sẵn sàng (giống nhau trên hai hệ điều hành):

```bash
docker info
```

```bash
docker compose version
```

Nếu `docker info` báo không kết nối được server, mở Docker Desktop và chờ engine chạy xong.

## 2. Tải và chạy CVAT

Đặt thư mục `cvat` của CVAT **cạnh** repo bài lab, trong thư mục `lab` ([SETUP.md](SETUP.md) mục 3), không đặt bên trong repo (repo bài lab có sẵn một thư mục `cvat/` nhỏ chỉ chứa file cấu hình, đừng nhầm hai thư mục này).

**Windows (PowerShell)**

```powershell
New-Item -ItemType Directory -Force $HOME\lab
cd $HOME\lab
git clone --branch v2.83.0 --depth 1 https://github.com/cvat-ai/cvat
cd cvat
docker compose up -d
docker compose ps
```

**macOS (Terminal)**

```bash
mkdir -p ~/lab && cd ~/lab
git clone --branch v2.83.0 --depth 1 https://github.com/cvat-ai/cvat
cd cvat
docker compose up -d
docker compose ps
```

Lần đầu Docker tải image khá lâu. Chạy lại `docker compose ps` đến khi mọi container ở trạng thái `Up` / `running`, không còn cái nào `Restarting`.

## 3. Tạo tài khoản

Giống nhau trên hai hệ điều hành, chạy trong thư mục `cvat` của CVAT:

```bash
docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
```

Nhập tên đăng nhập, email (có thể để trống) và mật khẩu. Khi gõ mật khẩu, màn hình không hiện ký tự nào; đó là bình thường. Cách khác: mở `http://localhost:8080/auth/register` và tự đăng ký. Mật khẩu này **chỉ dùng cho CVAT trên máy bạn**. Đừng dùng lại mật khẩu email hay LMS, và đừng gửi cho ai.

## 4. Kiểm tra

1. Mở Chrome hoặc Edge, vào `http://localhost:8080`.
2. Đăng nhập bằng tài khoản vừa tạo.
3. Thấy trang **Projects** hoặc **Tasks** là xong.
4. Bấm tên tài khoản ở góc phải → **About**: hộp thoại hiện *Server version* và *UI version* (2.83.0, hoặc 2.82.0 nếu dùng lại bản Ngày 12). Ghi số này vào `REPORT.md` mục 1.

## 5. Bật và tắt

Chạy trong thư mục `cvat` của CVAT, giống nhau trên hai hệ điều hành. **Máy dùng cấu hình máy yếu (mục 6) thì luôn dùng lệnh hai `-f` ở mục 6 thay cho lệnh dưới.**

Tắt khi không dùng, dữ liệu vẫn giữ:

```bash
docker compose stop
```

Bật lại, chờ khoảng 1 phút rồi mở `localhost:8080`:

```bash
docker compose up -d
```

**Đừng** chạy `docker compose down -v` trước khi nộp bài và có điểm: `-v` xoá toàn bộ task và cuboid đã vẽ.

## 6. Máy yếu (RAM 8 GB)

1. Docker Desktop → Settings → Resources: cấp 5–6 GB RAM, đóng bớt ứng dụng khác (trình duyệt nhiều tab, IDE, Zoom).
2. Windows (WSL 2) đặt giới hạn RAM bằng file `.wslconfig`. Mở file:

   ```powershell
   notepad $HOME\.wslconfig
   ```

   Ghi hai dòng sau, lưu lại:

   ```
   [wsl2]
   memory=6GB
   ```

   Rồi khởi động lại WSL và mở lại Docker Desktop:

   ```powershell
   wsl --shutdown
   ```

3. Chép file `cvat/docker-compose.lowspec.yml` của repo bài lab vào thư mục `cvat` của CVAT, rồi khởi động CVAT bằng hai file compose. File này giảm số tiến trình worker và không chạy Grafana (trang Analytics, bài lab không dùng).

   **Windows (PowerShell)**, đang đứng trong thư mục `cvat` của CVAT:

   ```powershell
   Copy-Item ..\K5-L23-DAY13-<MSHV>-PointCloudCuboid\cvat\docker-compose.lowspec.yml .
   docker compose -f docker-compose.yml -f docker-compose.lowspec.yml up -d --remove-orphans
   ```

   **macOS (Terminal)**, đang đứng trong thư mục `cvat` của CVAT:

   ```bash
   cp ../K5-L23-DAY13-<MSHV>-PointCloudCuboid/cvat/docker-compose.lowspec.yml .
   docker compose -f docker-compose.yml -f docker-compose.lowspec.yml up -d --remove-orphans
   ```

   Từ đây, mỗi lần bật lại CVAT cũng dùng đúng lệnh hai `-f` này. Lỡ chạy `docker compose up -d` thường thì Grafana bật lại; tắt nó bằng `docker stop cvat_grafana`.

4. Máy vẫn không chạy nổi Docker: báo coach để ngồi ghép đôi. Khi dùng chung máy, mỗi người đăng nhập tài khoản CVAT riêng và tạo task `D13-<MÃ SỐ>` riêng.

## 7. Tạo task bằng tay (khi `python scripts/lab.py task` không nối được CVAT)

Lệnh `task` gửi dữ liệu lên CVAT qua `cvat-sdk`. Nếu lệnh đó lỗi mà trình duyệt vẫn mở được CVAT, tạo task bằng tay:

1. Đóng gói đúng 10 frame của bạn thành một file zip (giống nhau trên Windows và macOS):

   ```bash
   python scripts/lab.py bundle
   ```

   Lệnh in đường dẫn file, dạng `work/D13-<MÃ SỐ>.zip` (khoảng 23 MB). Task chung của vòng hiệu chuẩn: `python scripts/lab.py bundle --code <MÃ CHUNG>`.
2. Trên CVAT, trang **Tasks**, bấm nút **+** màu xanh → **Create a new task**. Nếu menu không hiện, mở thẳng `http://localhost:8080/tasks/create`.
3. Ô **Name**: đúng `D13-<MÃ SỐ>`, ví dụ `D13-2A202600123`. Lệnh `report` tìm task theo tên này.
4. **Labels**: chọn tab **Raw**, xoá nội dung có sẵn, dán toàn bộ nội dung file [`cvat/labels.json`](../cvat/labels.json) của repo, bấm **Done**. Kết quả là 5 nhãn kiểu Cuboid: Car, Truck, Bus, Cyclist, Pedestrian, đúng chữ hoa, chữ thường.
5. **Select files → My computer**: chọn file zip ở bước 1. Kéo xuống, bấm **Submit & Open**.
6. Mở job, kiểm frame đầu trùng frame đầu mà `python scripts/lab.py dry` in ra.

Sau đó vẽ và xuất bảng A như bình thường (`python scripts/lab.py report`). Lệnh `report` vẫn cần `cvat-sdk` nối được CVAT.

## 8. Lỗi hay gặp khi cài

| Hiện tượng | Cách gỡ |
|---|---|
| `port is already allocated` (8080) | Có chương trình khác dùng cổng 8080. Tắt nó, hoặc hỏi coach cách đổi cổng |
| `localhost:8080` trắng trang hoặc 502 | Server chưa khởi động xong. Chờ 1–2 phút, `docker compose ps` xem còn container nào Restarting |
| `No such container: cvat_server` | Chạy `docker compose ps` để xem CVAT đã bật chưa và tên container đúng |
| `docker: command not found` / `is not recognized` | Docker Desktop chưa cài hoặc chưa mở; mở lại terminal sau khi cài |
| Windows: Docker báo *WSL 2 installation is incomplete* | Chạy `wsl --install` trong PowerShell quyền administrator, khởi động lại máy |
| Mac chip Apple: container thoát ngay, log có `exec format error` | Bật Rosetta (mục 1), cập nhật Docker Desktop |
| Máy rất chậm | Làm theo mục 6 |
| Lệnh `scripts/lab.py` in `Server version … is not compatible with SDK version …` | CVAT trên máy là 2.82 (từ Ngày 12), `cvat-sdk` là 2.83. Coach đã thử: tạo task, đọc nhãn, xuất bảng A vẫn đúng. Bỏ qua cảnh báo, đừng cài lại `cvat-sdk`; hoặc cập nhật CVAT lên 2.83 **trước** buổi học |

## 9. Dùng giao diện 3D (đọc trước, đỡ mất thời gian trong lớp)

Coach demo lại trên CVAT của lớp ở đầu Bước 3.

**Màn hình job 3D**

- Khung lớn là **khung 3D** (Perspective). Ba khung nhỏ **Top**, **Side**, **Front** ở dưới chỉ chiếu **cuboid đang chọn**, phóng quanh nó; chưa chọn cuboid nào thì chúng gần như trống.
- Muốn nhìn cả cảnh từ trên xuống: xoay khung 3D cho tới khi nhìn thẳng xuống, rồi thu nhỏ.
- Ảnh camera nằm bên phải. Mặc định chỉ hiện 3 ảnh: cam01, cam03, cam05. Rê chuột lên một khung ảnh, bấm biểu tượng bánh răng hiện ở góc khung để đổi sang camera khác (cam06–cam09). Lỡ đóng một khung ảnh thì dùng nút đặt lại bố cục trên thanh nhỏ của khu ảnh.

**Điều khiển khung 3D**

- Kéo chuột trái: xoay. Kéo chuột phải: dời. Con lăn: phóng to, thu nhỏ.
- Nháy đúp vào một cuboid: căn giữa và chọn nó. Nháy đúp chỗ trống: về góc nhìn mặc định.
- Các nút ở góc khung 3D: U, O dời camera lên, xuống; J, L dời sang trái, phải; I, K phóng to, thu nhỏ; bốn mũi tên xoay và nghiêng camera. Đây là cách chỉnh góc nhìn khi đang đặt hộp (lúc đó kéo chuột bị khoá).
- `F` / `D`: frame sau / trước. **Save** hoặc `Ctrl+S` (macOS: `Cmd+S`) sau mỗi frame.

**Vẽ và chỉnh cuboid**

- Thanh công cụ trái → nút vẽ cuboid → chọn label → bấm **Shape** (không bấm Track). Một hộp chạy theo con trỏ: đưa tới cụm điểm của vật rồi **nháy đúp** để đặt. `Esc` để huỷ. `N` vẽ tiếp một cuboid cùng label, cùng kiểu.
- Thẻ cuboid trong danh sách bên phải phải ghi **CUBOID SHAPE**. Ghi CUBOID TRACK là đã vẽ nhầm Track: xoá (chọn rồi bấm `Delete`) và vẽ lại; cuboid Track không vào bảng A.
- Chọn cuboid rồi chỉnh: ở **Top** dời tâm, kéo cạnh hoặc góc để đổi dài, rộng, kéo nút xoay để xoay yaw (ngược đầu xe thì xoay nửa vòng). Ở **Side**, **Front** chỉ dời hộp lên xuống và kéo cạnh để đáy chạm đường, đặt chiều cao. **Không xoay ở Side, Front**: hộp sẽ nghiêng mà bảng A không ghi độ nghiêng. Lỡ tay thì `Ctrl+Z` (macOS: `Cmd+Z`).
- Đổi label: ô chọn label trên thẻ cuboid.
- **Occluded**: nút hình một người trên thẻ cuboid (sau nút ổ khoá); bấm vào thành hình hai người là đã bật. Hoặc chọn cuboid rồi bấm `Q`.
- Mũi tên hướng: phần **Appearance** ở thanh bên phải, tích **Cuboid orientation** (dưới *Outlined borders*). Mỗi cuboid hiện 3 mũi tên: đỏ là trục dài, xanh lá là trục ngang, xanh dương hướng lên. Chỉ cần **mũi tên đỏ chỉ đầu xe**.
- CVAT của lớp không vẽ cuboid lên ảnh camera. Muốn xem cuboid trên 7 ảnh camera: `python scripts/lab.py preview` ([SELF_CHECK.md](SELF_CHECK.md)).
