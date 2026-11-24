# Checkpoints — Day 13

Bài cá nhân, buổi thực hành **16:00–20:00**. Mốc giờ là điểm **tự kiểm tra**, không phải hạn nộp. Chậm hơn mốc thì báo coach, đừng vẽ ẩu để đuổi kịp.

| Mốc | Mục tiêu | Tự kiểm tra |
|---|---|---|
| 16:25 | **CP1** Chuẩn bị | `python scripts/lab.py dry` in đủ 10 frame, mỗi frame `camera=7`; task `D13-<MÃ SỐ>` mở được, thấy point cloud và ảnh camera |
| 16:50 | **CP2** Đọc frame | Chỉ đúng phía trước (−y) và +x trên Top của frame đầu; đã kể được một vật phía sau hoặc hai bên; `REPORT.md` §2 có 2 frame đọc kỹ |
| 17:25 | **CP3** Frame 1 | `python scripts/lab.py report`: frame 1 có ≥ 8 cuboid; xe con có `length` > `width`; xe cùng chiều `yaw_deg` gần 270°; `z_bottom` quanh −1,7 m |
| 17:55 | **CP4** Frame 2–6 | Mỗi frame ≥ 5 cuboid; đã **Save** trước giờ nghỉ |
| 18:35 | **CP5** Frame 7–10 | Tổng ≥ 50 cuboid (nên 60–70); đã quét cả phía sau và hai bên |
| 19:00 | **CP6** Bốn hiện tượng | 4 ảnh và 4 dòng trong `REPORT.md` §4; nguyên nhân ghi là giả thuyết |
| 19:30 | **CP7** Tự kiểm + nộp | `python scripts/lab.py sync` đã chạy sau lần Save cuối; đã sửa ≥ 2 cuboid; `python scripts/check_submission.py` hết LỖI; `REPORT.md` xong |

Sau CP7: exit ticket cuối buổi (19:35), rồi 20' dự phòng để bắt kịp hoặc vẽ thêm.

## Cần hiểu ở mỗi mốc

**CP1.** Vì sao cùng một mã số luôn ra cùng 10 frame? Vì sao `--replace` nguy hiểm sau khi đã vẽ?

**CP2.** Vì sao phải biết phía trước là −y **trước** khi vẽ? Cái gì chỉ camera cho biết (màu, chữ trên biển, loại xe), cái gì chỉ LiDAR cho biết (khoảng cách, kích thước theo mét)? Vì sao cam01 không đủ để tìm hết vật?

**CP3.** Vì sao cuboid khớp ở Top vẫn có thể sai (lơ lửng, chìm)? `length` nằm dọc theo cái gì? Nếu `yaw_deg` của xe cùng chiều ra gần 90° thì bạn đã làm gì sai?

**CP4–CP5.** Vì sao vẽ vật gần trước? Vật thưa điểm: khi nào vẽ, khi nào bỏ qua? Vì sao "không đoán" lại tốt hơn "đoán cho xong" khi nhãn dùng để train model?

**CP6.** Bóng che khác thưa ở xa ở đâu? Vì sao nguyên nhân của điểm lạ chỉ nên ghi là giả thuyết?

**CP7.** Cuboid bị `selfcheck` cờ có chắc là sai không? Cuboid không bị cờ có chắc là đúng không? Vì sao phải chạy lại `report` sau mỗi lần sửa trên CVAT?
