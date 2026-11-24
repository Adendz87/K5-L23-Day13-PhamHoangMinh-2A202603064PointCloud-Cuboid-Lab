# Lệnh tắt. Chạy từ thư mục gốc repo. Windows không có make: chạy trực tiếp các lệnh python bên dưới.
# Chọn python chạy được thật (trên Windows, `python3` có thể chỉ là lối tắt mở Microsoft Store).
PY ?= $(shell for p in python3 python; do $$p -c "import sys" >/dev/null 2>&1 && { echo $$p; break; }; done)
export PYTHONUTF8=1

dry:             ## xem 10 frame của bạn, không nối CVAT (kiểm cài đặt và dữ liệu)
	$(PY) scripts/lab.py dry

task:            ## tạo task D13-<MÃ SỐ> trên CVAT (đã có thì chỉ in lại link, không tạo thêm)
	$(PY) scripts/lab.py task

bundle:          ## đóng gói 10 frame -> work/D13-<MÃ SỐ>.zip để tạo task bằng tay (docs/CVAT_SETUP.md mục 7)
	$(PY) scripts/lab.py bundle

report:          ## xuất bảng A từ cuboid đã Save -> submission/D13-<MÃ SỐ>-bangA.csv
	$(PY) scripts/lab.py report

preview:         ## vẽ cuboid của bạn lên 7 ảnh camera -> work/xem/
	$(PY) scripts/lab.py preview

selfcheck:       ## soát cuboid bằng point cloud -> submission/D13-<MÃ SỐ>-tukiem.csv (gợi ý, không chấm điểm)
	$(PY) scripts/lab.py selfcheck

sync:            ## report + preview + selfcheck (chạy sau mỗi lần Save lớn)
	$(PY) scripts/lab.py sync

pack:            ## nén bảng A, phiếu tự kiểm, ảnh chụp -> work/K5-L23-DAY13-<MÃ SỐ>-nop.zip (nộp LMS)
	$(PY) scripts/lab.py pack

check:           ## kiểm tra bài nộp: hết LỖI mới nộp
	$(PY) scripts/check_submission.py

all: sync check
