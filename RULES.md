# RULES — Lab Ngày 13

## 1. Làm cá nhân, ngồi theo cặp

- Mỗi bạn một mã số, một task CVAT `D13-<MÃ SỐ>`, một máy. **Điểm chấm theo từng người.**
- Mỗi mã số nhận 10 frame khác nhau, nên không có bài của ai để chép.
- Ngồi cạnh nhau theo cặp để đổi kiểm ở cuối buổi ([CHECKPOINTS.md](CHECKPOINTS.md), lần cuối).

| Được | Không được |
|---|---|
| Bàn với bạn về cách hiểu guideline, ca khó (gọi bằng tên frame, ví dụ "s02f07, xe trắng bên trái khoảng 10 m"), lỗi CVAT, lỗi cài đặt | Vẽ hộ cuboid trên task của bạn, hoặc nhờ bạn vẽ hộ |
| Xem nhờ frame của bạn cho T4 khi frame của mình thiếu hiện tượng, **ghi rõ mượn của ai** | Chép bảng A hoặc báo cáo của bạn rồi nộp là của mình |
| Nhờ bạn kiểm lại con số trong báo cáo | Dùng mã số của người khác để tạo task |

Các bạn vẽ giống nhau chỉ cho thấy **nhất quán**, không chứng minh cuboid **đúng**. Guideline và coach mới là căn cứ phân xử.

## 2. Dữ liệu ở yên trong lớp

1. `data-VF` chỉ nằm trên máy bạn và trong CVAT của lớp (CVAT local hoặc máy chủ coach phát). Không tải lên Drive cá nhân, GitHub, chatbot AI, hay CVAT online.
2. **Không gửi ảnh camera, ảnh chụp màn hình point cloud vào nhóm chat hay mạng xã hội.** Hỏi bằng tên frame.
3. Ảnh chụp màn hình cho báo cáo chỉ nộp qua LMS, không đưa lên repo công khai.
4. Bảng A và phiếu tự kiểm chỉ chứa số của cuboid bạn vẽ, nên đổi cho bạn bên cạnh để kiểm chéo được.
5. `.gitignore` của repo đã chặn `data-VF/`, ảnh, file `.bin`, `.pcd`, `.zip`, thư mục `nop/` và `xem/`. Đừng sửa các dòng đó, đừng dùng `git add -f`.
6. Hết khóa, xóa thư mục `data-VF` và `xem/` trên máy.

Lý do: dữ liệu VF là dữ liệu lái xe thực tế của dự án, chỉ được dùng trong lớp. Ảnh camera có người và biển số thật.

## 3. Mật khẩu

- Mật khẩu CVAT chỉ nhập tay khi lệnh hỏi, hoặc đặt biến `CVAT_PASSWORD` cho cửa sổ terminal đang mở ([COMMANDS.md](COMMANDS.md) mục 6).
- **Không ghi mật khẩu vào file**, không dán vào báo cáo, không gửi cho bạn hay coach. Khi cần người khác tạo task giúp, bạn tự gõ mật khẩu.
- Không dùng lại mật khẩu email hay LMS cho CVAT.

## 4. Dùng AI

- **Được** hỏi AI về lệnh Python, PowerShell, Terminal, Docker, cách dùng CVAT, hoặc cách hiểu một khái niệm (yaw, BEV, intensity…).
- **Không được** đưa ảnh camera, ảnh chụp màn hình hay file point cloud cho AI. Không nhờ AI vẽ cuboid, viết sẵn dòng nhận xét T4 hay điền số T5.
- Ghi mọi lần dùng AI vào `prompts.md` (mẫu ở [templates/prompts.md](templates/prompts.md)): công cụ, câu hỏi, bạn dùng kết quả thế nào. Không dùng AI thì ghi "Không dùng".

## 5. Khi kẹt

1. Tra [COMMON_ERRORS.md](COMMON_ERRORS.md).
2. Hỏi bạn bên cạnh (bằng tên frame).
3. Giơ tay hỏi coach. Kẹt cài đặt quá 5 phút thì ghép với bạn bên cạnh để không lỡ phần đọc frame.

Ca guideline không nói tới: ghi frame và mô tả vào báo cáo rồi hỏi coach. Đừng tự đặt luật mới, đừng đoán.

**Không sửa bảng A bằng tay.** Bảng A phải khớp với task CVAT của bạn. Muốn đổi số thì sửa cuboid trên CVAT, Save, rồi chạy lại `report`.

## 6. Không tự xóa task

- `--replace` xóa task cùng mọi cuboid. Chỉ dùng khi chưa vẽ gì, hoặc khi coach bảo.
- Không chạy `docker compose down -v` cho tới khi đã có điểm.

## 7. Nộp muộn và sửa sau hạn

- Hạn nộp ghi ở [SUBMISSION.md](SUBMISSION.md). Coach thông báo trên LMS nếu có thay đổi.
- Nộp sau hạn bị trừ điểm theo quy định chung của khóa. Nộp muộn vẫn tốt hơn không nộp.
- Sau hạn, không sửa cuboid trong task `D13-<MÃ SỐ>`. Lỗi phát hiện thêm thì ghi vào mục 7 của báo cáo.
