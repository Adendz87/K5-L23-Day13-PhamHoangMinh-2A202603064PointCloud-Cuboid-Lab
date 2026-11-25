# Báo cáo Day 13 — Phạm Hoàng Minh, 2A202603064

## 1. Kết luận trước

- MSSV: `2A202603064`

- Task CVAT: `D13-2A202603064`, Task ID: `31`

- Hệ điều hành: macOS

- CVAT Server: `2.82.1`

- Trình duyệt: Chrome

- MSSV người ngồi cạnh: 03319

Sau khi bổ sung các đối tượng Pedestrian và Cyclist trong CVAT và đồng bộ lại, bảng A có tổng cộng **81 cuboid** trên 10 frame.

| Frame | Số cuboid |

|---|---:|

| s01f26 | 17 |

| s01f53 | 8 |

| s02f22 | 9 |

| s02f51 | 5 |

| s03f04 | 11 |

| s03f53 | 7 |

| s04f39 | 8 |

| s04f55 | 6 |

| s05f13 | 7 |

| s05f48 | 3 |

| **Tổng** | **81** |

Theo bảng A sau đồng bộ: 74 Car, 2 Bus, 2 Truck, 1 Pedestrian và 2 Cyclist.

Frame ít cuboid nhất là `s05f48`, có 3 cuboid. `/image/t1-s05f48.png`, Frame s05f48 có mật độ point rất thấp, dữ liệu 3D không đủ để xác định thêm các đối tượng. Do đó, chỉ gán nhãn được 3 cuboid có thể nhận diện rõ ràng.

Phiếu tự kiểm sau khi đồng bộ lại ghi nhận **18/81 cuboid có cảnh báo**. Các cảnh báo là gợi ý cần đối chiếu trực quan, không phải kết luận chắc chắn cuboid sai.

s01f26 (`t1-s01f26-3d.png`). Các point trong frame phân bố khá rõ ràng, mật độ điểm tốt, giúp tôi dễ dàng nhận diện hình dạng và ranh giới của các đối tượng 3D. Vì vậy, tôi tự tin nhất về việc xác định vị trí, hướng yaw và kích thước cuboid trong frame này.

Phần tôi còn chưa chắc: một số cụm point của Pedestrian/Cyclist khá nhỏ và thưa nên cần thận trọng khi xác định kích thước, ranh giới và hướng yaw. Tôi chỉ tạo cuboid khi có đủ cơ sở nhận diện từ point cloud.

### Cách sử dụng CVAT

- Đổi góc nhìn: kết hợp xoay point cloud để quan sát đối tượng từ nhiều hướng khác nhau. Đồng thời, sử dụng thao tác kéo và di chuyển chuột để thay đổi góc nhìn, phóng to hoặc thu nhỏ nhằm quan sát rõ hình dạng và vị trí các đối tượng.

- Vẽ và chỉnh cuboid: chọn công cụ Shape và sử dụng Cuboid để tạo khung 3D bao quanh đối tượng. Sau khi tạo cuboid, tôi nháy đúp vào cuboid để chỉnh sửa. Tôi kết hợp các góc nhìn Top, Side và Front để điều chỉnh vị trí, chiều dài, chiều rộng, chiều cao và hướng của cuboid sao cho phù hợp với point cloud.

- sử dụng ảnh 2D để đối chiếu vị trí và hướng của đối tượng, kiểm tra xem cuboid có bao quanh đúng đối tượng hay không. Sau đó, chuyển sang Top View để quan sát và điều chỉnh hướng xoay (yaw) của cuboid sao cho phù hợp với chiều thực tế của đối tượng trong point cloud.

## 2. Đọc frame (Bước 2)

Hai frame đọc kỹ: 0, 1

Ảnh minh chứng:

Ảnh minh chứng:

- `t1-s01f26-3d.png` — Point cloud 3D của frame s01f26, dùng để quan sát tổng thể các đối tượng và mật độ point.

- `t1-s01f26-top.png` — Góc nhìn Top View của frame s01f26, dùng để xác định hướng các trục tọa độ và hướng của đối tượng.

- `t1-s01f53-3d.png` — Point cloud 3D của frame s01f53, dùng để quan sát hình dạng và vị trí các đối tượng.

- `t1-s01f53-top.png` — Góc nhìn Top View của frame s01f53, dùng để xác định hướng các trục tọa độ và hỗ trợ xác định yaw.

| Frame | Phía trước, +x, +y trên Top View | Mặt đường | Vật xa nhất | Loại vật thấy | Vật phía sau/hai bên | Cụm chưa đọc được |

|---|---|---|---|---|---|---|

| s01f26 | Khu vực ngã tư, có nhiều nhánh đường giao nhau. Hướng phía trước, +X và +Y chưa xác định chính xác. | Mặt đường tương đối bằng phẳng, không thấy độ dốc đáng kể. | Khoảng 30 m (ước lượng). | Car, Bus. | Hai bên đường có dải phân cách và hàng cây. Các phương tiện và đối tượng ở gần có point khá rõ. | Các cụm point ở xa có mật độ thưa, một số gần như mất hẳn trong point cloud 3D nhưng vẫn có thể quan sát trên ảnh camera 2D. |

| s01f53 | Khu vực đường tương đối thẳng. Hướng phía trước, +X và +Y chưa xác định chính xác. | Mặt đường tương đối bằng phẳng, không thấy độ dốc đáng kể. | Khoảng 20 m (ước lượng). | Car. | Hai bên đường có dải phân cách và hàng cây. Các phương tiện và đối tượng ở gần có point khá rõ. | Các cụm point ở xa có mật độ thưa, một số gần như mất hẳn trong point cloud 3D nhưng vẫn có thể quan sát trên ảnh camera 2D. |

### Camera và LiDAR

Ba điều camera cho biết rõ hơn:

1. Màu sắc và đặc điểm bên ngoài của phương tiện, người đi bộ và người đi xe đạp, hỗ trợ phân biệt class khi hình ảnh đủ rõ.

2. Hình dáng tổng thể của phương tiện, giúp phân biệt các loại đối tượng, trong đó có người đi bộ và người đi xe đạp khi hình ảnh đủ rõ.

3. Các phương tiện ở xa hoặc bị thiếu point trên LiDAR vẫn có thể nhận diện rõ hơn qua hình ảnh camera 2D.

Ba điều LiDAR cho biết rõ hơn:

1. Khoảng cách và vị trí 3D của các đối tượng như Car, Bus, Pedestrian và Cyclist.

2. Chiều dài, chiều rộng và chiều cao thực tế của phương tiện, hỗ trợ tạo cuboid.

3. Hướng, vị trí tương đối và độ sâu của phương tiện, hỗ trợ xác định vị trí và góc xoay yaw của cuboid.

### Tám frame còn lại

| Frame | Phía trước ở cạnh nào của Top View | Điều lạ |

|---|---|---|

| s01f53 | Từ trái sang phải | Không có |

| s02f22 | Từ phải sang trái | Có Pedestrian được gán cuboid sau khi kiểm tra lại CVAT. |

| s02f51 | Từ dưới lên trên | Không có |

| s03f04 | Từ trái sang phải | Có Cyclist được gán cuboid sau khi kiểm tra lại CVAT. |

| s03f53 | Từ trái sang phải | Có Cyclist được gán cuboid sau khi kiểm tra lại CVAT. |

| s04f39 | Từ phải sang trái | Không có |

| s04f55 | Từ phải sang trái | Không có |

| s05f13 | Từ dưới lên trên | Không có |

| s05f48 | Từ trái sang phải | Không có |

**## 3. Ba cuboid có hướng dẫn (Bước 3)**

Ảnh minh chứng:

- `t2-a-car.png` — `images/t2-a-car.png`

- `t2-b-bus-truck.png` — `images/t2-b-bus-truck.png`

- `t2-c-ped-cyclist.png` — Ảnh minh chứng cần thể hiện Pedestrian ở frame s02f22 và Cyclist ở frame s03f04 hoặc s03f53. Lưu ảnh chụp màn hình CVAT vào đúng đường dẫn `report/individual/images/t2-c-ped-cyclist.png`.

| Vật | Frame, idx | Class | Mũi tên yaw đúng? | Đáy chạm đường? | Đã kiểm Top/Side/Front và ảnh? | Kích thước |

|---|---|---|---|---|---|---|

| (a) Xe con gần | s03f04, idx 2 | Car | Đã tự xoay và căn chỉnh yaw theo hướng thân xe trên Top View | Gần sát mặt đường; ground_gap = -0.03 m | Đã kiểm tra đầy đủ Top/Side/Front và ảnh camera | 4.37 × 2.11 × 1.60 m; nằm trong khoảng kích thước Car (dài 3.0–6.0 m, rộng 1.4–2.3 m, cao 1.2–2.3 m) |

| (b) Xe buýt hoặc xe tải | s03f53, idx 5 | Bus | Đã tự xoay và căn chỉnh yaw theo hướng thân xe trên Top View | Gần mặt đường; ground_gap = 0.11 m | Đã kiểm tra đầy đủ Top/Side/Front và ảnh camera | 11.99 × 2.79 × 2.83 m; chiều rộng nằm trong khoảng Bus 2.0–3.2 m; cần đối chiếu chiều dài và chiều cao với bảng 4.3 |

| (c) Người đi bộ | s02f22 (cuboid mới bổ sung) | Pedestrian | Kiểm tra theo hướng thân người trên Top View; cần đối chiếu lại trực quan trước khi chốt | Kiểm tra đáy cuboid so với mặt đường trong CVAT | Đối chiếu point cloud và ảnh camera; kiểm tra Top/Side/Front | Đã bổ sung 1 cuboid Pedestrian vào bảng A. Chưa có số đo kích thước được trích xuất trong nội dung báo cáo này. |\n| (d) Người đi xe đạp | s03f04 #11; s03f53 #7 | Cyclist | Phiếu tự kiểm cảnh báo length < width ở cả hai cuboid; cần kiểm tra lại mũi tên yaw theo trục dọc xe đạp | Kiểm tra đáy cuboid so với mặt đường trong CVAT | Đối chiếu point cloud và ảnh camera; kiểm tra Top/Side/Front | Đã bổ sung 2 cuboid Cyclist. Kích thước hiện bị cảnh báo: s03f04 #11 length=0.61 m, width=1.56 m; s03f53 #7 length=0.49 m. Cần kiểm tra lại hướng yaw và kích thước, không tự suy đoán số đo đúng. |

## Hiệu chuẩn và trường hợp bỏ qua**

- Cuboid của tôi khác với các bạn ở: Chưa có thông tin về điểm khác biệt sau khi so sánh.

- Guideline cả lớp thống nhất: lấy cả gương  car, các vật thể không xác định được trong 3d nhưng thấy trong 2d không lấy.

- - Đối tượng bỏ qua: Một số đối tượng ở xa có mật độ point cloud quá thấp, số lượng point không đủ để xác định rõ hình dạng, kích thước và class nên không thực hiện gán nhãn. Lý do: LOW_VISIBILITY.

## 4. Bốn hiện tượng chất lượng point cloud (Bước 4)

- `t4-1-bong-che.png` — `images/t4-1-bong-che.png`

- `t4-2-thua-o-xa.png` — `images/t4-2-thua-o-xa.png`

- `t4-3-phan-xa-thap.png` — `images/t4-3-phan-xa-thap.png`

- `t4-4-diem-la.png` — `images/t4-4-diem-la.png`

| Hiện tượng | Frame / tên ảnh / nguồn | Nguyên nhân (giả thuyết) | Quan sát point cloud | Hệ quả khi gán nhãn |

|---|---|---|---|---|

| Bóng che | `images/che_khuat.png` | Vật thể ở phía trước có thể chắn đường truyền tia LiDAR đến vật thể phía sau. | Một phần vật thể phía sau có thể bị thiếu điểm hoặc không hiển thị đầy đủ. | Khó xác định ranh giới và kích thước cuboid của vật thể bị che khuất. |

| Thưa ở xa | s01f26, s01f53; ảnh Top View và point cloud 3D | Mật độ điểm LiDAR giảm khi khoảng cách đến cảm biến tăng. | Các cụm điểm của phương tiện ở xa thưa hơn, một số gần như biến mất trong point cloud 3D nhưng vẫn có thể quan sát trên ảnh camera 2D. | Khó xác định chính xác kích thước, hình dạng và ranh giới cuboid của phương tiện ở xa. |

| Phản xạ thấp | `images/phan_xa_thap.png` | Bề mặt vật thể có thể phản xạ tín hiệu LiDAR yếu, khiến cảm biến thu được ít điểm. | Chưa có vùng point cloud cụ thể được xác nhận là do phản xạ thấp. | Không nên tự suy đoán phần hình dạng bị thiếu để mở rộng cuboid. |

| Điểm lạ | s01f26, cuboid Car số 3 và số 11; kết quả tự kiểm | Có thể do sai lệch khi đặt cuboid, nhiễu điểm hoặc mặt đường không được xác định chính xác. | Cuboid số 3 có đáy cao hơn mặt đường 0.55 m; cuboid số 11 có đáy thấp hơn mặt đường 0.44 m. | Cần kiểm tra lại vị trí đáy và sự phù hợp giữa cuboid với mặt đường, tránh để hộp bị lơ lửng hoặc chìm. |

Lưu ý: nguyên nhân là giả thuyết, không phải kết luận đã được xác minh. Nếu dùng frame từ task chung hoặc của bạn khác, ghi rõ nguồn.

## 5. Số đo từ cuboid của tôi (Bước 5)

Dữ liệu lấy từ bảng A và phiếu tự kiểm. z đáy được tính bằng z − height/2.

| Cuboid (frame, idx, class) | z (m) | h (m) | z đáy (m) | dist_m | r (m) | yaw_deg | points_in |

|---|---:|---:|---:|---:|---:|---:|---:|

| s03f04 / idx 2 / Car | -1.05 | 1.52 | -1.81 | 3.58 | 3.73 | 269.5° | 2190 |

| s04f55 / idx 3 / Car | -1.00 | 1.56 | -1.78 | 15.58 | 15.61 | 89.9° | 814 |

| s01f26 / idx 17 / Bus | 0.35 | 2.37 | -0.84 | 45.88 | 45.89 | 267.3° | 139 |

### Cuboid gần nhất và xa nhất

- Gần nhất: **s03f04 / idx 2 / Car**, dist_m = 3.58 m, r = 3.73 m.

- Xa nhất: **s01f26 / idx 17 / Bus**, dist_m = 45.88 m, r = 45.89 m.

**### Kích thước đại diện**

- Xe con gần nhất trong CSV: s03f04 / idx 2 / Car.

  Kích thước: length = 4.37 m, width = 2.11 m, height = 1.60 m. Cả ba thông số đều nằm trong khoảng kích thước Car theo bảng 4.3 (dài 3.0–6.0 m, rộng 1.4–2.3 m, cao 1.2–2.3 m).

- Pedestrian/Cyclist: bảng A mới đã có 1 Pedestrian ở s02f22 và 2 Cyclist ở s03f04, s03f53. Báo cáo chưa ghi số đo đại diện vì cần trích xuất chính xác length, width, height, dist_m và points_in của ba cuboid từ bảng A mới nhất.

  Không có đối tượng phù hợp để thực hiện so sánh kích thước.

 Xe Bus/Truck gần nhất: s03f53 / idx 5 / Bus.

  Kích thước: length = 11.99 m, width = 2.79 m, height = 2.83 m. Chiều rộng 2.79 m nằm trong khoảng kích thước Bus (2.0–3.2 m). Chiều dài và chiều cao cần đối chiếu với khoảng quy định tương ứng trong bảng 4.3.

### Kiểm tra hướng xe

- Cuboid có yaw gần 270° nhất: s01f53 / idx 2 / Car, yaw = 270.4°.

  Hướng xoay của cuboid gần 270°.

- Cuboid có yaw gần 90° nhất: s04f55 / idx 3 / Car, yaw = 89.9°.

  Hướng xoay của cuboid gần 90°.

**### Mật độ điểm theo khoảng cách**

| Cuboid | dist_m | points_in |

|---|---:|---:|

| s03f04 / idx 2 / Car | 3.58 | 2190 |

| s02f51 / idx 3 / Car | 11.42 | 1195 |

| s01f26 / idx 5 / Car | 21.46 | 547 |

| s01f26 / idx 17 / Bus | 45.88 | 139 |

Nhận xét:

Mật độ điểm có xu hướng giảm khi khoảng cách từ đối tượng đến cảm biến LiDAR tăng. Cụ thể, cuboid gần nhất ở khoảng cách 3.58 m có 2190 điểm, trong khi cuboid xa nhất ở khoảng cách 45.88 m chỉ có 139 điểm.

Khoảng cách tăng khoảng 12.8 lần, nhưng số điểm chỉ còn khoảng 6.35% so với ban đầu, tức giảm khoảng 15.8 lần. Ở các khoảng cách trung gian, số điểm cũng giảm dần: từ 1195 điểm tại 11.42 m xuống 547 điểm tại 21.46 m và còn 139 điểm tại 45.88 m.

Kết quả này phù hợp với xu hướng trong slide:

- 0–10 m: 1968 điểm.

- 10–20 m: 718 điểm.

- 20–30 m: 214 điểm.

- 30–40 m: 72 điểm.

- 60–80 m: 19 điểm.

Như vậy, đối tượng càng xa cảm biến thì số lượng point thu được càng giảm, khiến point cloud thưa hơn và việc xác định hình dạng, kích thước cũng như ranh giới cuboid trở nên khó khăn hơn.

**### Cảnh báo tự kiểm**

Có 18 cảnh báo trên 81 cuboid. Danh sách dưới đây được cập nhật theo phiếu tự kiểm sau khi đồng bộ lại:

- s01f26 idx 3 (Car): đáy cao hơn mặt đường 0.55 m (lơ lửng?).

- s01f26 idx 10 (Car): width=2.40 ngoài khoảng 1.4–2.3 của Car.

- s01f26 idx 11 (Car): đáy thấp hơn mặt đường 0.44 m (chìm?).

- s01f26 idx 16 (Car): length=1.96 ngoài khoảng 3.0–6.0 của Car; width=3.67 ngoài khoảng 1.4–2.3 của Car; length < width: cần kiểm tra hướng yaw.

- s01f26 idx 17 (Bus): width=3.21 ngoài khoảng 2.0–3.2 của Bus.

- s02f22 idx 7 (Car): 43 điểm sát ngay ngoài mép cuboid (quá chật hoặc có vật bên cạnh?).

- s02f22 idx 8 (Car): đáy cao hơn mặt đường 0.48 m (lơ lửng?).

- s03f04 idx 10 (Truck): length=2.99 ngoài khoảng 4.0–18.0 của Truck.

- s03f04 idx 11 (Cyclist): length=0.61 ngoài khoảng 1.0–2.4 của Cyclist; width=1.56 ngoài khoảng 0.3–1.2; length < width, cần kiểm tra hướng yaw.

- s03f53 idx 4 (Car): length=7.01 ngoài khoảng 3.0–6.0 của Car; width=3.13 ngoài khoảng 1.4–2.3 của Car; height=2.79 ngoài khoảng 1.2–2.3 của Car.

- s03f53 idx 6 (Car): đáy thấp hơn mặt đường 0.28 m (chìm?); height=0.85 ngoài khoảng 1.2–2.3 của Car.

- s03f53 idx 7 (Cyclist): length=0.49 ngoài khoảng 1.0–2.4 của Cyclist; length < width, cần kiểm tra hướng yaw.

- s04f39 idx 6 (Car): width=2.52 ngoài khoảng 1.4–2.3 của Car.

- s04f39 idx 8 (Car): width=1.30 ngoài khoảng 1.4–2.3 của Car.

- s04f55 idx 6 (Car): đáy cao hơn mặt đường 0.78 m (lơ lửng?).

- s05f13 idx 1 (Car): width=2.32 ngoài khoảng 1.4–2.3 của Car.

- s05f13 idx 3 (Car): đáy cao hơn mặt đường 0.85 m (lơ lửng?).

- s05f48 idx 2 (Car): width=2.56 ngoài khoảng 1.4–2.3 của Car; height=2.41 ngoài khoảng 1.2–2.3 của Car.

Nhận xét:

Các cảnh báo là kết quả kiểm tra tự động dựa trên kích thước, vị trí đáy và số lượng point nằm ngoài cuboid. Đây là những trường hợp cần chú ý khi kiểm tra chất lượng, không đồng nghĩa tất cả cuboid đều bị gán nhãn sai. Một số sai lệch có thể xuất phát từ hình dạng thực tế, góc quan sát, mật độ point hoặc cách đặt cuboid.

Hai cuboid đã sửa sau khi xem preview/selfcheck:

1. Cuboid thứ nhất: Đã kiểm tra, chưa thấy vấn đề nên giữ nguyên.

2. Cuboid thứ hai: Đã kiểm tra, chưa thấy vấn đề nên giữ nguyên.

Frame `s05f48` có 3 cuboid. Do mật độ point cloud thấp, chỉ có 3 đối tượng có đủ điểm để nhận diện và xác định cuboid. Những cụm điểm còn lại không đủ rõ ràng để xác định chắc chắn đối tượng và thực hiện gán nhãn bổ sung.

### Kiểm chéo

**### Kiểm chéo**

- MSSV người kiểm chéo: 03319-PHẠM VŨ TÙNG DƯƠNG

- Số liệu thứ nhất: Hai bên cùng thảo luận và đối chiếu số liệu thứ nhất.

- Số liệu thứ hai: Hai bên cùng thảo luận và đối chiếu số liệu thứ hai.

- Kết quả: Hai bên đã cùng nhau thảo luận, kiểm tra và đối chiếu kết quả. 

## 6. Ý nghĩa của nhãn, cách dùng AI và điều còn chưa chắc

Nhãn 3D được đo bằng mét thay vì pixel vì cuboid cần thể hiện vị trí, kích thước và hướng của vật thể trong không gian thực. Điều này giúp mô hình học hình học và khoảng cách giữa các vật thể, không chỉ vị trí trên ảnh 2D.

Vật ở xa thường có mật độ điểm thấp hơn, làm ranh giới và hình dạng khó xác định. Vì vậy, cần quy tắc riêng cho các vùng thưa điểm để tránh tạo nhãn thiếu cơ sở hoặc suy diễn kích thước không chính xác.

**### Sử dụng AI**

- Công cụ: ChatGPT.

- Nội dung hỗ trợ:

  - Đọc và giải thích yêu cầu của bài Point Cloud Cuboid Lab.

  - Hướng dẫn quy trình thực hiện từng bước trên CVAT.

  - Hỗ trợ xác định hướng phía trước trên Top View.

**### Điều còn chưa chắc**

- Một số đối tượng ở xa có mật độ point cloud thấp, khiến việc xác định chính xác hình dạng và ranh giới cuboid khó khăn hơn.

- Đối với các đối tượng có điểm bị che khuất hoặc cụm điểm không rõ ràng, chưa thể xác định đầy đủ kích thước thực tế.

- Hướng yaw và chiều dài, chiều rộng của một số cuboid cần được đối chiếu với hình dạng thực tế của phương tiện để tránh đặt sai hướng.

- Một số trường hợp class hoặc kích thước đối tượng khó xác định khi point cloud quá thưa. Với Pedestrian ở s02f22 và Cyclist ở s03f04, s03f53, cần tiếp tục đối chiếu hướng yaw và kích thước vì phiếu tự kiểm đang cảnh báo hai cuboid Cyclist có length nhỏ hơn width.