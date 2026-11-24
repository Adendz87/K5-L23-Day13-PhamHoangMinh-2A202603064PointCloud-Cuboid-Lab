# GUIDE — Lab Ngày 13: đọc point cloud VF và vẽ cuboid trên CVAT 3D

Lệnh của từng bước nằm ở [COMMANDS.md](COMMANDS.md). File này nói bạn **làm gì và vì sao**.

## 1. Bạn sẽ làm được gì sau buổi này

1. Tự dựng task CVAT 3D từ dữ liệu VF bằng một lệnh, mở job và đổi giữa các view 3D, Top, Side, Front và ảnh camera.
2. Đọc một frame theo năm bước: gốc và trục, mặt đất, tầm và góc nhìn, ảnh camera, quét cảnh.
3. Vẽ cuboid 7 tham số (cx, cy, cz, l, w, h, yaw) đúng class, đúng hướng, đáy chạm mặt đường, kích thước hợp lý.
4. Nhận ra bốn hiện tượng làm hỏng point cloud (bóng che, thưa ở xa, phản xạ thấp, điểm lạ) trên dữ liệu thật và nói được hệ quả khi gán nhãn.
5. Đọc lại 7 số, khoảng cách từ chính cuboid của mình (bảng A), tự kiểm kích thước và độ cao đáy.

Ba điều cần mang về:

- **Đọc trước, vẽ sau.** Sai hướng trục hay sai mặt đất thì mọi cuboid đều lệch.
- **Ba view, một vật.** Cuboid chỉ đúng khi khớp ở cả Top, Side và Front. Một view không đủ.
- **Biết khi nào không chắc.** Bóng che, vật thưa điểm, phản xạ thấp, điểm lạ là chỗ guideline bảo "hỏi coach, không đoán".

## 2. Quy ước của buổi (đọc trước)

### 2.1. Hệ tọa độ VF

Gốc ở tâm LiDAR trên nóc xe, đơn vị mét, bàn tay phải.

| Trục | Chiều dương | Ghi nhớ |
|---|---|---|
| x | sang **trái** | bên phải xe là −x |
| y | ra **sau** | phía trước xe là **−y** |
| z | **lên** | mặt đường khoảng z = −1,7 m (LiDAR cao khoảng 1,7 m) |

Ví dụ: điểm (x, y, z) = (+6, −20, −1,7) nằm trên mặt đường, 20 m phía trước và 6 m bên trái.

Hệ này khác KITTI và ROS (x tiến, y trái). Nếu bạn đã quen hệ khác, kiểm lại bằng ảnh cam01: cam01 nhìn về phía trước xe, tức hướng −y.

### 2.2. Cuboid 7 tham số

`(cx, cy, cz, l, w, h, yaw)`: tâm cuboid; dài (dọc theo hướng yaw), rộng, cao; yaw quanh trục z, đo từ +x (trái), ngược chiều kim đồng hồ nhìn từ trên.

- Xe cùng chiều phía trước: yaw ≈ **270°**.
- Xe đi ngược chiều: yaw ≈ **90°**.

### 2.3. Camera

| Camera | Nhìn về |
|---|---|
| cam01, cam03 | phía trước (cam03 là ống tele) |
| cam06 | trước-trái |
| cam07 | trước-phải |
| cam05 | sau-trái |
| cam08 | sau-phải |
| cam09 | phía sau |

LiDAR phủ 360°, mỗi camera chỉ phủ một hình quạt. **Vật phía sau và hai bên không có trong ảnh cam01**: tìm chúng ở view Top rồi đối chiếu camera nhìn về hướng đó.

### 2.4. Vùng vẽ và số lượng

- Vẽ trong vùng **360° quanh xe, xa ≤ 50 m** (khoảng mười một thân xe con nối nhau theo mọi hướng).
- Mỗi frame trung bình có khoảng 18 vật trong vùng này. **Không ai vẽ hết.** Vẽ theo thứ tự vật gần → xa, vật rõ và dày điểm trước.
- Tối thiểu: frame 1 từ **8** cuboid, mỗi frame sau từ **5** cuboid, tổng từ **50**.
- Mục tiêu nên nhắm: frame 1 **10** cuboid, mỗi frame sau **6** cuboid, tổng 60–70. Vẽ đúng mức tối thiểu thì độ phủ chỉ vừa sát ngưỡng đạt (xem [RUBRIC.md](RUBRIC.md)).
- Coach chấm độ phủ chủ yếu trên vật ≤ 30 m. Vẽ thừa không bị trừ điểm.
- **Không vẽ xe của chính mình** (xe thu dữ liệu, ngay tại gốc tọa độ).

### 2.5. Khác biệt giữa lab hôm nay và guideline đầy đủ

Guideline 3D Cuboid viết cho bài gán nhãn chính thức theo track. Hôm nay bạn làm quen công cụ, nên:

| Guideline đầy đủ | Lab Ngày 13 |
|---|---|
| Phạm vi ≤ 100 m | ≤ 50 m, ưu tiên ≤ 30 m |
| Cuboid dạng Track, nội suy, khóa kích thước theo track | Cuboid dạng **Shape** trên từng frame. Frame của bạn không liên tiếp nhau nên không có nội suy |
| Khoảng 60 frame liên tiếp | 10 frame rời, 2 frame mỗi sequence |
| Tạo issue trên CVAT cho ca không chắc | Ghi frame và mô tả vào báo cáo, hỏi coach |

Mọi quy tắc còn lại (class, hình dạng cuboid, hướng, đáy, sai số, vật thưa điểm) áp dụng nguyên.

## 3. Tóm tắt guideline 3D Cuboid

Bản đầy đủ có hình minh họa: [guideline/3D_Cuboid_Annotation_Guideline.docx](guideline/3D_Cuboid_Annotation_Guideline.docx).

### 3.1. Năm class, không thêm, không đổi tên

| Class | Gồm | Không gồm |
|---|---|---|
| **Car** | Xe chủ yếu chở người: sedan, hatchback, wagon, van, minivan, SUV, jeep; taxi, xe cảnh sát, cấp cứu thân xe con | Xe bán tải, xe chở hàng (→ Truck) |
| **Truck** | Xe chở hàng hoặc xe chuyên dụng cỡ lớn: **bán tải**, xe tải, xe ben, đầu kéo, van chở hàng, xe công trình. Rơ-moóc cũng là Truck, **vẽ cuboid riêng** tách khỏi đầu kéo | |
| **Bus** | Xe buýt thường, xe buýt nối toa, xe khách lớn, minibus chở khách | |
| **Pedestrian** | Người đi bộ ở mọi tư thế; **người dắt xe đạp, xe máy** | Người đang lái hoặc ngồi trên xe hai bánh (→ Cyclist), người trong xe, mannequin, tượng |
| **Cyclist** | Xe đạp, xe đạp điện, xe máy, xe tay ga, xe ba bánh **có người lái**. Cuboid gồm cả xe và người | |

### 3.2. Quy tắc cuboid

1. **Hình dạng:** mỗi vật một cuboid riêng, bao trọn các điểm LiDAR của vật, gồm phần chìa ra và phần bị che suy luận được. Không bao dư quá mức.
2. **Hướng:** yaw theo hướng chuyển động, hoặc theo đầu xe nếu đứng yên. **Mũi tên đỏ chỉ đầu xe.**
3. **Đáy:** chạm mặt đường, không lơ lửng, không chìm.
4. **Kiểm:** đối chiếu trên Top, Side, Front.
5. **Sai số cho phép** trên ba view: Car, Bus, Truck **±5%**; Pedestrian, Cyclist **±10%** so với kích thước đúng.
6. **Vật thưa điểm:** thấy được khoảng 15–20% thể tích cuboid thì vẽ. Ít hơn thì chỉ vẽ khi có đủ cơ sở suy luận (ảnh camera rõ, hình dạng nhận ra được); không thì bỏ qua và ghi vào báo cáo.
7. **Occluded:** bật khi vật bị vật khác che một phần. Cuboid vẫn bao trọn phần suy luận được.

### 3.3. Bảng 4.3 — kích thước tham chiếu (mét)

Dùng để kiểm kích thước có hợp lý không, nhất là khi vật thưa điểm. Point cloud và ảnh camera vẫn là bằng chứng chính.

| Loại | Class | Dài | Rộng | Cao |
|---|---|---|---|---|
| Sedan, hatchback | Car | 3,8 – 5,0 | 1,70 – 1,90 | 1,40 – 1,60 |
| SUV, minivan, van chở người | Car | 4,4 – 5,3 | 1,80 – 2,10 | 1,65 – 2,10 |
| Bán tải | Truck | 5,2 – 6,2 | 1,85 – 2,10 | 1,80 – 2,00 |
| Xe tải hộp, xe tải nhẹ | Truck | 5,5 – 9,0 | 2,00 – 2,55 | 2,40 – 3,50 |
| Xe tải nặng, đầu kéo | Truck | 6,0 – 12,0 | 2,40 – 2,60 | 3,00 – 4,00 |
| Rơ-moóc sau đầu kéo | Truck | 8,0 – 16,0 | 2,50 – 2,60 | 3,50 – 4,10 |
| Rơ-moóc nhỏ (sau xe con) | Truck | 2,0 – 5,0 | 1,50 – 2,20 | 0,80 – 2,50 |
| Máy xúc, cần cẩu, xe lu | Truck | 4,0 – 12,0 | 2,00 – 3,20 | 2,50 – 4,00 |
| Xe buýt thường | Bus | 10,0 – 12,5 | 2,50 – 2,60 | 3,00 – 3,50 |
| Xe buýt nối toa | Bus | 17,0 – 18,5 | 2,50 – 2,60 | 3,00 – 3,40 |
| Người lớn | Pedestrian | 0,4 – 0,9 | 0,5 – 0,9 | 1,50 – 1,95 |
| Trẻ em | Pedestrian | 0,3 – 0,6 | 0,3 – 0,6 | 0,90 – 1,40 |
| Xe đạp có người | Cyclist | 1,6 – 1,9 | 0,50 – 0,70 | 1,60 – 1,90 |
| Xe máy có người | Cyclist | 1,8 – 2,3 | 0,70 – 0,95 | 1,40 – 1,80 |
| Xe ba bánh có người | Cyclist | 2,5 – 3,5 | 1,00 – 1,50 | 1,50 – 2,00 |

### 3.4. Khi không chắc

Không đoán cho xong. Ghi lại frame, vị trí đại khái và loại nghi vấn, rồi hỏi coach:

| Loại nghi vấn | Ví dụ |
|---|---|
| UNCERTAIN_CLASS | Car hay Truck (van chở hàng, bán tải); Bus hay Truck; Pedestrian hay Cyclist (dắt xe hay đang lái) |
| UNCERTAIN_SCOPE | Vật quanh ngưỡng 50 m; vật quá thưa điểm |
| ATTRIBUTE_CHECK | Không chắc có occluded hay không |
| LOW_VISIBILITY | Vật khó quan sát do đêm, mưa, ngược sáng, quá xa hoặc quá ít điểm |

## 4. Lịch buổi thực hành

| Giờ | Việc | Phút |
|---|---|---|
| 16:00–16:10 | Điểm danh, chữa exit ticket buổi sáng | 10 |
| 16:10–16:25 | **P0** · Thiết lập, tạo task, mở job | 15 |
| 16:25–16:50 | **T1** · Đọc năm bước trên 2 frame đầu, lướt 8 frame còn lại (chưa vẽ) | 25 |
| 16:50–17:25 | **T2** · Coach demo, vòng hiệu chuẩn cả lớp, vẽ có hướng dẫn trên frame 1 | 35 |
| 17:25–17:55 | **T3a** · Vẽ frame 2–6, khoảng 6 phút mỗi frame | 30 |
| 17:55–18:10 | Nghỉ (nhớ **Save** trước khi nghỉ) | 15 |
| 18:10–18:35 | **T3b** · Vẽ frame 7–10 | 25 |
| 18:35–19:00 | **T4** · Săn bốn hiện tượng chất lượng | 25 |
| 19:00–19:15 | **T5** · Xuất bảng A, tự kiểm, đọc số | 15 |
| 19:15–19:30 | Hoàn thiện báo cáo, kiểm chéo với bạn bên cạnh, nộp | 15 |
| 19:30–19:40 | Chốt và exit ticket cuối buổi | 10 |
| 19:40–20:00 | Buffer: bắt kịp, vẽ thêm, sửa cuboid kém | 20 |

Coach có thể chỉnh nhịp trong buổi.

## 5. Nhiệm vụ

### P0 · Thiết lập (15 phút)

1. Mở terminal, vào thư mục repo, kích hoạt `.venv` ([COMMANDS.md](COMMANDS.md) mục 0).
2. Chạy lệnh tạo task ([COMMANDS.md](COMMANDS.md) mục 2), nhập mật khẩu khi được hỏi. Lệnh in tên 10 frame và đường dẫn task.
3. Mở đường dẫn trong Chrome hoặc Edge, đăng nhập, vào job. Bạn phải thấy point cloud và ảnh camera.
4. Chép `templates/report.md` thành file báo cáo của bạn ([COMMANDS.md](COMMANDS.md) mục 7) và điền mục 0.

Tên frame dạng `s02f07` nghĩa là sequence 02, frame chỉ số 7 (đếm từ 0). Kẹt quá 5 phút thì ghép với bạn bên cạnh, coach xử lý sau.

### T1 · Đọc năm bước và làm quen các view (25 phút)

**Chưa vẽ.** Đi kỹ trên 2 frame đầu, khoảng 8 phút mỗi frame, đủ năm bước. Lướt 8 frame còn lại, khoảng 1 phút mỗi frame: phía trước ở đâu, có vật gì phía sau và hai bên, có điểm lạ không.

1. **Gốc và trục:** mở view Top. Dựa vào ảnh cam01 (nhìn về phía trước xe), tìm phía nào của view Top là phía trước (−y). Đánh dấu +x (trái), +y (sau) lên ảnh chụp Top.
2. **Mặt đất:** mở Side. Mặt đường phẳng hay dốc? Đường nằm thấp hơn LiDAR bao nhiêu (ước bằng mắt; số đo chính xác ở T5)?
3. **Tầm và góc nhìn:** vật xa nhất bạn còn nhận ra khoảng bao xa? Phần nào của cảnh ảnh camera không thấy?
4. **Ảnh camera:** đổi giữa các camera. Ghi 3 điều chỉ camera cho biết và 3 điều chỉ LiDAR cho biết.
5. **Quét cảnh:** liệt kê loại vật thấy (xe, xe buýt, xe máy, người, cột, cây, nhà) và ít nhất một cụm điểm bạn chưa đọc được.

Chụp một ảnh view 3D và một ảnh Top cho mỗi frame đọc kỹ. Điền bảng 2 của báo cáo.

### T2 · Vẽ cuboid có hướng dẫn trên frame 1 (35 phút)

**Coach demo** vẽ một xe (khoảng 10 phút). Xem hết rồi mới vẽ.

**Vòng hiệu chuẩn** (khoảng 10 phút): cả lớp vẽ cùng 3 vật trên một frame chung do coach chỉ định, không trao đổi, rồi so cuboid **giữa các bạn với nhau**. Coach chiếu độ lệch lớn nhất và cả lớp bàn 2 bất đồng lớn nhất. Ba cuboid này không chấm điểm. Điều cần nhớ: các bạn vẽ giống nhau chỉ cho thấy **nhất quán**, chưa chắc **đúng**. Guideline và coach mới là căn cứ.

**Vẽ ba vật mẫu** trên frame đầu tiên của task: **(a)** một xe con gần nhất, **(b)** một xe buýt hoặc xe tải, **(c)** một người đi bộ hoặc xe hai bánh. Frame thiếu loại nào thì lấy ở frame 2.

Checklist cho từng cuboid:

1. Chọn class đúng theo mục 3.1 (bán tải là Truck; xe máy có người là Cyclist; dắt xe là Pedestrian).
2. Cuboid bao trọn các điểm của vật, gồm phần bị che suy ra được; không bao dư.
3. Bật orientation: mũi tên đỏ chỉ đầu xe. Xe cùng chiều phía trước thì mũi tên cùng hướng xe mình, xe ngược chiều thì ngược lại.
4. Đáy cuboid chạm mặt đường: kiểm ở Side và Front.
5. Kiểm cả ba view Top, Side, Front, rồi đối chiếu ảnh camera để chắc class và hướng.
6. So kích thước với bảng 4.3. Vật bị che một phần: bật occluded.
7. Vật rất thưa điểm: áp quy tắc 15–20%. Không đủ cơ sở thì bỏ qua và ghi vào báo cáo.

Sau ba vật mẫu, hoàn thiện các vật gần còn lại của frame 1 đến khi có **từ 8 cuboid, nên 10**. Coach xem cuboid đầu tiên của mỗi bạn. Hai lỗi hay gặp nhất là mũi tên ngược và đáy lơ lửng.

Về "biểu tượng vàng chiếu box lên ảnh" trong guideline: tùy bản CVAT, tính năng này có thể không có. Nếu CVAT của bạn không chiếu được, dùng ảnh camera để nhận loại vật và hướng, đo kích thước ở Top, Side, Front, và dùng lệnh `preview` ở T5 để xem cuboid của mình trên 7 ảnh camera.

### T3 · Vẽ chín frame còn lại (55 phút, nghỉ ở giữa)

1. Mỗi frame khoảng 6 phút: frame 2–6 trước giờ nghỉ, frame 7–10 sau giờ nghỉ. **Hết giờ của frame thì sang frame sau, không dồn.**
2. Mỗi frame từ **5 cuboid, nên 6**, theo thứ tự vật gần → xa, vật rõ và dày điểm trước.
3. Quét view Top theo vòng tròn quanh xe. Đừng bỏ sót vật gần ở phía sau và hai bên.
4. Vật thưa điểm theo quy tắc 15–20% không bắt buộc vẽ. Vật không chắc class thì không đoán: ghi frame và mô tả để dùng ở T4.
5. **Save sau mỗi frame.**

### T4 · Săn bốn hiện tượng chất lượng (25 phút)

Mỗi hiện tượng cần **một ảnh chụp từ CVAT** và **một dòng**: nguyên nhân (giả thuyết) → thấy gì trên point cloud → việc gán nhãn bị ảnh hưởng thế nào theo guideline. Frame của bạn không có hiện tượng nào thì xem nhờ frame của bạn bên cạnh và ghi rõ mượn của ai.

| # | Hiện tượng | Tìm gì | Guideline nói gì |
|---|---|---|---|
| 1 | **Bóng che** | Vùng ít hoặc không có điểm phía sau xe buýt, xe tải, xe đỗ, tường. Có vật nào bị che không? | Bật occluded, cuboid bao phần suy luận được |
| 2 | **Thưa ở xa** | Một xe cách khoảng 30–50 m, chỉ còn vài chục hoặc vài điểm | Vẽ nếu thấy khoảng 15–20% thể tích hoặc suy luận được; không thì bỏ qua, ghi LOW_VISIBILITY |
| 3 | **Phản xạ thấp hoặc ít điểm bất thường** | Xe tối màu, kính, hoặc vật ít điểm hơn hẳn vật cùng tầm. Xem ảnh camera | Ghi giả thuyết, không khẳng định |
| 4 | **Điểm lạ** | Điểm hoặc cụm điểm không thuộc vật nào: trên cao, lẻ loi, giữa không khí, hoặc **dưới mặt đường** | Không gán thành vật |

Frame tham khảo coach đã dò sẵn. Nếu task của bạn có frame nào trong danh sách thì mở ra xem:

| Hiện tượng | Frame | Nhìn ở đâu |
|---|---|---|
| Bóng che | `s02f00`, `s03f00` | s02f00: xe buýt đỏ sát bên trái, khoảng 4 m, che hẳn một góc phía sau nó. s03f00: tường quây công trình bên trái, khoảng 6 m |
| Điểm lạ | `s02f35`, `s05f56` | Cụm điểm nằm sâu **dưới** mặt đường, phía sau bên trái. Xoay nghiêng view 3D mới thấy rõ |
| Intensity cao | `s04f02`, `s02f00`, `s02f49` | Biển báo, biển số xe: điểm sáng hơn hẳn xung quanh |

Điểm "dưới mặt đất" là sai hình học chắc chắn, nhưng nguyên nhân thì chưa rõ. Khi viết, ghi là giả thuyết.

### T5 · Đọc số từ chính cuboid của bạn (15 phút)

1. **Save** trong CVAT. Chạy `report` để xuất bảng A ([COMMANDS.md](COMMANDS.md) mục 3). Mở `nop/D13-<MÃ SỐ>-bangA.csv` bằng bảng tính.
2. Chạy `preview` và `check` ([COMMANDS.md](COMMANDS.md) mục 4–5). Sửa ít nhất 2 cuboid trên CVAT, Save, rồi chạy lại `report`. Cách đọc kết quả ở [CHECKPOINTS.md](CHECKPOINTS.md).
3. **Mặt đường:** với 3 cuboid, tính z đáy = z − h/2 và so với cột `z_bottom`. Mặt đường khoảng −1,7 m. Lệch hơn 0,3 m nghĩa là cuboid lơ lửng hoặc chìm: sửa trong CVAT.
4. **Khoảng cách:** chọn cuboid gần nhất và xa nhất. Ghi `dist_m` (khoảng cách trên mặt đường, √(x² + y²)) và tự tính r = √(x² + y² + z²).
5. **Kích thước:** với một người đi bộ (hoặc xe hai bánh) và một xe con, so l, w, h với bảng 4.3. Chiều nào ngoài khoảng, vì sao?
6. **Hướng:** xe cùng chiều phía trước có `yaw_deg` gần 270°, xe ngược chiều gần 90°. Đối chiếu với cuboid của bạn.
7. **Mật độ theo khoảng cách:** chọn 4 cuboid ở các `dist_m` khác nhau. Lấy số điểm trong cuboid từ cột `points_in` của phiếu tự kiểm (`-tukiem.csv`) và viết một câu quy luật. So với số của bài giảng: xe con trung vị khoảng 1968 điểm ở 0–10 m, 718 ở 10–20 m, 214 ở 20–30 m, 72 ở 30–40 m.

Các cột của bảng A:

| Cột | Ý nghĩa |
|---|---|
| `frame`, `idx`, `label` | Tên frame, số thứ tự cuboid trong frame, class |
| `x`, `y`, `z` | Tâm cuboid theo hệ VF (x trái, y sau, z lên), mét |
| `length`, `width`, `height` | Dài (dọc mũi tên yaw), rộng, cao, mét |
| `yaw_rad`, `yaw_deg` | Góc yaw, `yaw_deg` trong 0–360° |
| `z_bottom` | z − height/2, độ cao đáy cuboid |
| `dist_m`, `dist_bin` | √(x² + y²) và khoảng cách theo bin: 0–10, 10–20, 20–30, 30–50 |
| `az_deg` | Góc phương vị của tâm: 0° thẳng phía trước, dương lệch trái, âm lệch phải, ±180° phía sau |
| `occluded` | 1 nếu bạn đã bật occluded |

## 6. Trước khi nộp — checklist chất lượng

- [ ] Chỉ 5 class, gán đúng theo mục 3.1.
- [ ] Mỗi cuboid bao trọn điểm, đáy chạm đường, mũi tên đỏ chỉ đầu xe; đã kiểm ở Top, Side, Front và ảnh camera.
- [ ] Occluded bật đúng chỗ.
- [ ] Ca không chắc đã ghi vào báo cáo, không đoán.
- [ ] Đã Save job và chạy lại `report` sau lần sửa cuối.
- [ ] Đã soát toàn bộ 10 frame hai lần.

Nộp theo [SUBMISSION.md](SUBMISSION.md).
