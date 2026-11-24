# Cài CVAT trên máy cá nhân (làm trước buổi học)

Mục tiêu: máy bạn mở được `http://localhost:8080` và đăng nhập được CVAT. Cài lần đầu mất khoảng 20–40 phút, tuỳ mạng.

Phiên bản lớp dùng: **CVAT v2.83.0**. Nếu máy bạn còn CVAT từ Ngày 12 (v2.82.0) đang chạy tốt, bạn dùng tiếp được, không cần cài lại.

Nếu coach thông báo lớp dùng **máy chủ CVAT chung**, bỏ qua file này. Đổi `cvat_host` trong `configs/lab.ini` thành địa chỉ coach phát.

Nguồn: https://docs.cvat.ai/docs/administration/basics/installation/

## 1. Cần có

- **Docker Desktop** đã cài ([SETUP.md](SETUP.md) mục 2) và **đang mở**, biểu tượng cá voi báo *Engine running*.
- **Git**, **Chrome hoặc Edge**, khoảng 10 GB đĩa trống.
- RAM cho Docker: khoảng 8 GB nếu máy có 16 GB. Máy 8 GB xem mục 6.
- **Mac chip Apple (M1 trở lên):** Docker Desktop → Settings → General → bật **Use Rosetta for x86_64/amd64 emulation**. Image `cvat/server` chỉ có bản amd64.

Kiểm Docker đã sẵn sàng (giống nhau trên hai hệ điều hành):

```bash
docker info
```

```bash
docker compose version
```

Nếu `docker info` báo không kết nối được server, mở Docker Desktop và chờ engine chạy xong.

## 2. Tải và chạy CVAT

Đặt thư mục `cvat` của CVAT **cạnh** repo bài lab, không đặt bên trong (repo bài lab có sẵn một thư mục `cvat/` nhỏ chỉ chứa file cấu hình).

**Windows (PowerShell)**

```powershell
cd $HOME\Documents
git clone --branch v2.83.0 --depth 1 https://github.com/cvat-ai/cvat
cd cvat
docker compose up -d
docker compose ps
```

**macOS (Terminal)**

```bash
cd ~/Documents
git clone --branch v2.83.0 --depth 1 https://github.com/cvat-ai/cvat
cd cvat
docker compose up -d
docker compose ps
```

Lần đầu Docker tải image khá lâu. Chạy lại `docker compose ps` đến khi mọi container ở trạng thái `Up` / `running`, không còn cái nào `Restarting`.

## 3. Tạo tài khoản

Giống nhau trên hai hệ điều hành, chạy trong thư mục `cvat`:

```bash
docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
```

Nhập tên đăng nhập, email (có thể để trống) và mật khẩu. Khi gõ mật khẩu, màn hình không hiện ký tự nào; đó là bình thường. Mật khẩu này **chỉ dùng cho CVAT trên máy bạn**. Đừng dùng lại mật khẩu email hay LMS, và đừng gửi cho ai.

## 4. Kiểm tra

1. Mở Chrome hoặc Edge, vào `http://localhost:8080`.
2. Đăng nhập bằng tài khoản vừa tạo.
3. Thấy trang **Projects** hoặc **Tasks** là xong.

## 5. Bật và tắt

Chạy trong thư mục `cvat`, giống nhau trên hai hệ điều hành.

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

1. Docker Desktop → Settings → Resources: cấp 5–6 GB RAM, đóng bớt ứng dụng khác.
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

3. Chép file `cvat/docker-compose.lowspec.yml` của repo bài lab vào thư mục `cvat`, rồi khởi động CVAT bằng hai file compose. File này giảm số tiến trình worker và không chạy Grafana (trang Analytics, bài lab không dùng).

   **Windows (PowerShell)**, đang đứng trong thư mục `cvat`:

   ```powershell
   Copy-Item ..\K5-L23-DAY13-<MSHV>-PointCloudCuboid\cvat\docker-compose.lowspec.yml .
   docker compose -f docker-compose.yml -f docker-compose.lowspec.yml up -d --remove-orphans
   ```

   **macOS (Terminal)**, đang đứng trong thư mục `cvat`:

   ```bash
   cp ../K5-L23-DAY13-<MSHV>-PointCloudCuboid/cvat/docker-compose.lowspec.yml .
   docker compose -f docker-compose.yml -f docker-compose.lowspec.yml up -d --remove-orphans
   ```

4. Máy vẫn không chạy nổi Docker: báo coach để ngồi ghép đôi. Khi dùng chung máy, mỗi người đăng nhập tài khoản CVAT riêng và tạo task `D13-<MÃ SỐ>` riêng.

## 7. Lỗi hay gặp khi cài

| Hiện tượng | Cách gỡ |
|---|---|
| `port is already allocated` (8080) | Có chương trình khác dùng cổng 8080. Tắt nó, hoặc hỏi coach cách đổi cổng |
| `localhost:8080` trắng trang hoặc 502 | Server chưa khởi động xong. Chờ 1–2 phút, `docker compose ps` xem còn container nào Restarting |
| `No such container: cvat_server` | Chạy `docker compose ps` để xem CVAT đã bật chưa và tên container đúng |
| `docker: command not found` / `is not recognized` | Docker Desktop chưa cài hoặc chưa mở; mở lại terminal sau khi cài |
| Windows: Docker báo *WSL 2 installation is incomplete* | Chạy `wsl --install` trong PowerShell quyền administrator, khởi động lại máy |
| Mac chip Apple: container thoát ngay, log có `exec format error` | Bật Rosetta (mục 1), cập nhật Docker Desktop |
| Máy rất chậm | Làm theo mục 6 |

## 8. Mẹo dùng giao diện 3D (đọc trước, đỡ mất thời gian trong lớp)

Vị trí chính xác các nút có thể khác giữa các bản CVAT. Coach demo lại trên bản của lớp ở đầu Bước 3.

- Màn hình job 3D có bốn khung: **Perspective** (view 3D) và ba khung chiếu **Top**, **Side**, **Front** của vật đang chọn. Ảnh camera nằm trong khung ảnh liên quan (context image).
- Vẽ cuboid: chọn công cụ cuboid ở thanh bên trái, chọn label, bấm **Shape** (không chọn Track), rồi bấm vào vật trong view 3D. Sau đó chỉnh vị trí, kích thước và góc xoay ở Top, Side, Front.
- Đổi label của một cuboid trong danh sách đối tượng bên phải. Ô **occluded** cũng ở đó.
- Bật mũi tên hướng: mở phần **Appearance** ở thanh bên phải, tích **orientation**. Mũi tên đỏ phải chỉ đầu xe.
- `F` / `D` chuyển frame sau / trước. Lưu thường xuyên bằng nút **Save** hoặc `Ctrl+S` (macOS: `Cmd+S`).
- Xoay view 3D bằng chuột trái, lăn con lăn để phóng to, thu nhỏ.
