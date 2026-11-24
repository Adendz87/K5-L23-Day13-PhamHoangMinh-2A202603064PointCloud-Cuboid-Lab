# Bốn hiện tượng làm hỏng point cloud (Bước 4)

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
