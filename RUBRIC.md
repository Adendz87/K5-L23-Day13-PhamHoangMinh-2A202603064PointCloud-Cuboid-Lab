# Rubric — 100 điểm

Điểm dựa trên **bằng chứng trong repo và trong task CVAT**, không dựa vào việc bạn vẽ được nhiều hay ít cờ tự kiểm. Báo cáo **trung thực** những cuboid còn chưa chắc, có phân tích, vẫn được điểm tốt.

> Trạng thái: đề xuất của Lab Coach. Trọng số và ngưỡng đạt chính thức do GV/VinUni quyết định và có thể được chỉnh sau buổi học.

| # | Hạng mục | Điểm | Bằng chứng |
|---|---|---:|---|
| 1 | Cuboid (chấm tự động so với nhãn chuẩn) | 40 | `submission/D13-<MÃ SỐ>-bangA.csv`, task CVAT |
| 2 | Đọc frame năm bước | 10 | `REPORT.md` §2, 4 ảnh |
| 3 | Ba cuboid có hướng dẫn | 10 | `REPORT.md` §3, 3 ảnh |
| 4 | Bốn hiện tượng chất lượng | 16 | `REPORT.md` §4, 4 ảnh |
| 5 | Số từ cuboid của bạn | 14 | `REPORT.md` §5, bảng A, phiếu tự kiểm |
| 6 | Báo cáo, kỷ luật dữ liệu, hợp tác | 10 | `REPORT.md` §1, §6, `check_submission.py`, commit |

## 1. Cuboid (40)
Chấm tự động từ bảng A, trong vùng 360° quanh xe, ≤ 50 m. Một cuboid được **ghép** với một vật khi hai hình chữ nhật nhìn từ trên xuống chồng nhau từ 50% (BEV-IoU ≥ 0,5); mỗi cuboid ghép nhiều nhất một vật.
- 15: **độ phủ** `recall_30m` = tỉ lệ vật **trong 30 m** bạn vẽ và ghép được. Điểm = 15 × min(1, recall_30m / 0,6).
- 10: **độ khớp** `IoU_tb` = IoU trung bình của các cuboid đã ghép. 0 điểm ở 0,5; đủ 10 điểm từ 0,75; tuyến tính ở giữa.
- 5: **class**: 5 × tỉ lệ cuboid đã ghép có đúng class.
- 5: **hướng**: số cuboid đã ghép bị ngược đầu. 0 cuboid: 5 · 1 cuboid: 3 · 2 cuboid: 1 · từ 3: 0.
- 5: **đáy và kích thước**: 2,5 nếu đáy lệch trung bình ≤ 0,2 m; 2,5 nếu sai kích thước trung bình ≤ 15% (một nửa nếu ≤ 25%).
- Vẽ thừa và vẽ vật xa hơn 30 m không bị trừ. Cuboid lệch quá nửa diện tích coi như chưa vẽ. Xe của chính mình không được chấm.

## 2. Đọc frame năm bước (10)
- 8: hai frame đọc kỹ, mỗi frame 4 điểm: nói đúng phía trước (−y) và hướng +x, chỉ đúng trên ảnh Top (2); loại vật và cụm chưa đọc được hợp lý, **không bịa** (1); có nhắc vật phía sau hoặc hai bên (1).
- 2: tám frame lướt ghi đúng phía trước.

## 3. Ba cuboid có hướng dẫn (10)
- 9: ba cuboid mẫu (xe con, xe buýt hoặc xe tải, người hoặc xe hai bánh), mỗi cuboid 3 điểm: class đúng, mũi tên yaw đúng, đáy chạm đường.
- 1: bảng mục 3 điền đủ, có ghi vật bỏ qua vì không đủ cơ sở (hoặc "không có").

## 4. Bốn hiện tượng chất lượng (16)
Mỗi hiện tượng 4 điểm:
- 2: đúng vật hoặc vùng, có ảnh chụp từ CVAT.
- 1: nguyên nhân hợp lý và **ghi rõ là giả thuyết**.
- 1: hệ quả nối đúng quy tắc guideline (occluded, quy tắc 15–20%, LOW_VISIBILITY, không gán điểm lạ thành vật).
- Frame mượn của bạn khác vẫn được điểm nếu ghi rõ mượn của ai.

## 5. Số từ cuboid của bạn (14)
- 3: ba z đáy tính đúng (z − h/2), có nhận xét lơ lửng, chìm hay chạm đường.
- 3: khoảng cách cuboid gần nhất và xa nhất, cả `dist_m` và r.
- 3: so kích thước một người (hoặc xe hai bánh) và một xe con với bảng 4.3, giải thích chiều nằm ngoài khoảng.
- 3: bốn cuboid mật độ và một câu quy luật theo khoảng cách.
- 2: đọc đúng yaw của xe cùng chiều và ngược chiều.
- Số trong báo cáo được đối chiếu với bảng A và phiếu tự kiểm trong repo.

## 6. Báo cáo, kỷ luật dữ liệu, hợp tác (10)
- 2: đủ 11 ảnh chụp, nộp qua LMS, **không** có dữ liệu VF trong repo.
- 2: mọi con số có đơn vị (m, °).
- 2: bảng A nộp đúng hạn, khớp task CVAT, không sửa tay; `check_submission.py` hết LỖI.
- 2: hai câu "để làm gì" (`REPORT.md` §6) nói từ phía model học trên nhãn này.
- 2: đổi kiểm với bạn bên cạnh; coach quan sát 2 lần trong buổi.
- Bị trừ nặng: bảng A không khớp task (sửa tay, lấy của người khác); commit dữ liệu VF hoặc ảnh camera lên repo public.

## Điều kiện đạt
Đạt khi thỏa **tất cả**: tổng ≥ 60 điểm · `recall_30m` ≥ 0,4 · không quá 2 cuboid ngược đầu · tổng từ 50 cuboid · đã nộp bảng A và `REPORT.md` đủ mục 2–5.

## Không chấm
- Ba cuboid của vòng hiệu chuẩn đầu Bước 3.
- Cảnh báo của `selfcheck`: còn cờ không bị trừ, hết cờ không được cộng.
- Phần "điều còn chưa chắc" ở `REPORT.md` §6 và phần vẽ thêm trong 20' dự phòng.

## Cách chấm trên máy coach
- Coach chạy công cụ chấm của mình trên bảng A trong repo (và đối chiếu với task CVAT khi coach xem được task). Nhãn chuẩn không phát cho học viên.
- Ghi đè các file "ĐÃ VIẾT SẴN" bằng bản gốc (so `scripts/_protected.json`), rồi chạy lại `check_submission.py`.
- Sau khi chốt bài nộp, coach có thể phát **phiếu hồ sơ lỗi** cho từng người: số cuboid đúng, ngược hướng, sai class, vẽ lệch, bỏ sót, và độ phủ theo khoảng cách.

## Nhất quán chưa phải là đúng
Bạn và bạn bên cạnh vẽ giống nhau chỉ cho thấy hai người **nhất quán**. Coach chấm theo guideline và nhãn chuẩn, không theo số đông.
