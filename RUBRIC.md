# RUBRIC — Lab Ngày 13

> **Trạng thái:** đề xuất của Lab Coach. Trọng số và ngưỡng đạt chính thức do **GV/VinUni** quyết định và có thể được chỉnh sau buổi học. Điểm dùng để phản hồi, không phải điểm thi.

Chấm **từng người**. Tổng 100 điểm: 40 điểm phần vẽ chấm tự động, 60 điểm coach chấm từ báo cáo.

## Phần vẽ — 40 điểm, chấm tự động từ bảng A

Coach so cuboid của bạn với nhãn chuẩn trong vùng 360° quanh xe, ≤ 50 m. Một cuboid được tính là **ghép đúng** với một vật khi hai hình chữ nhật nhìn từ trên xuống chồng nhau từ 50% (BEV-IoU ≥ 0,5). Mỗi cuboid ghép với nhiều nhất một vật.

| Tiêu chí | Cách đo | Điểm |
|---|---|---|
| Độ phủ (`recall_30m`) | Tỉ lệ vật **trong 30 m** bạn vẽ và ghép đúng. Điểm = 15 × min(1, recall_30m / 0,6) | 15 |
| Độ khớp (`IoU_tb`) | IoU trung bình của các cuboid đã ghép. 0 điểm ở 0,5; đủ 10 điểm từ 0,75; tuyến tính ở giữa | 10 |
| Class | 5 × tỉ lệ cuboid đã ghép có đúng class | 5 |
| Hướng (yaw) | Số cuboid đã ghép bị ngược đầu: 0 cuboid được 5; 1 được 3; 2 được 1; từ 3 được 0 | 5 |
| Đáy và kích thước | 2,5 nếu đáy lệch trung bình ≤ 0,2 m; 2,5 nếu sai kích thước trung bình ≤ 15% (một nửa nếu ≤ 25%) | 5 |

Điều rút ra cho cách vẽ:

- **Vật gần quan trọng nhất.** Độ phủ chỉ tính trên vật ≤ 30 m. Vẽ thừa và vẽ vật xa hơn không bị trừ.
- **Vẽ lệch thì coi như chưa vẽ.** Cuboid chồng dưới 50% với vật không được ghép, nên không cộng vào độ phủ.
- **Mức tối thiểu 8/5 chỉ vừa sát ngưỡng đạt.** Nhắm 10 cuboid ở frame 1 và 6 cuboid ở mỗi frame sau.
- Xe của chính mình (ngay tại gốc tọa độ) không được chấm. Đừng vẽ.

## Phần báo cáo — 60 điểm, coach chấm tay

| Tiêu chí | Đạt khi | Điểm |
|---|---|---|
| T1 · Đọc frame | Hai frame đọc kỹ, mỗi frame 4 điểm: nói đúng phía trước (−y) và hướng +x, chỉ đúng trên ảnh Top (2); loại vật và cụm chưa đọc được hợp lý, không bịa (1); có nhắc vật phía sau hoặc hai bên (1). Tám frame lướt: phía trước đúng (2) | 10 |
| T2 · Cuboid có hướng dẫn | Ba cuboid mẫu: class đúng, mũi tên yaw đúng, đáy chạm đường (3 điểm mỗi cuboid). Bảng 3 điền đủ (1) | 10 |
| T4 · Bốn hiện tượng | Mỗi hiện tượng 4 điểm: đúng vật hoặc vùng, có ảnh (2); nguyên nhân hợp lý và ghi rõ là giả thuyết (1); hệ quả nối đúng quy tắc guideline (1) | 16 |
| T5 · Số từ cuboid | Ba z đáy tính đúng, có nhận xét lơ lửng hay chìm (3); khoảng cách gần nhất, xa nhất và r (3); so kích thước với bảng 4.3 (3); bốn cuboid mật độ và câu quy luật (3); đọc yaw (2) | 14 |
| Báo cáo và kỷ luật dữ liệu | Đủ ảnh chụp (2); số có đơn vị (2); bảng A nộp đúng hạn và khớp task (2); hai câu "để làm gì" nói từ phía model (2) | 8 |
| Hợp tác | Đổi kiểm với bạn bên cạnh; coach quan sát 2 lần trong buổi | 2 |

## Điều kiện đạt

Đạt khi thỏa **tất cả**:

- Tổng ≥ 60 điểm.
- `recall_30m` ≥ 0,4.
- Không quá 2 cuboid ngược đầu.
- Tổng từ 50 cuboid.
- Đã nộp bảng A và báo cáo đủ mục 2–5.

## Không chấm

- Ba cuboid của vòng hiệu chuẩn đầu T2.
- Cảnh báo của lệnh `check`. Cờ chỉ để bạn xem lại; còn cờ không bị trừ, hết cờ không được cộng.
- Mục 7 của báo cáo (điều còn chưa chắc) và phần làm thêm trong buffer.

## Nhất quán chưa phải là đúng

Bạn và bạn bên cạnh vẽ giống nhau chỉ cho thấy hai người **nhất quán**. Coach chấm theo guideline và nhãn chuẩn, không theo số đông.
