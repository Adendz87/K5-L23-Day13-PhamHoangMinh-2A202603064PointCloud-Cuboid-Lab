#!/usr/bin/env python3
"""Tự kiểm tra bài nộp trước khi push (ĐÃ VIẾT SẴN). `python scripts/check_submission.py` — hết LỖI mới nộp.

Script chỉ kiểm bài nộp có ĐỦ và NHẤT QUÁN không. Nó không biết đáp án và không chấm cuboid của bạn đúng hay sai.
"""
from __future__ import annotations

import configparser
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cvat_lab"))
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

import vf_common as vf  # noqa: E402
from vf_cvat import TABLE_A_FIELDS  # noqa: E402

MIN_TOTAL, MIN_FIRST, MIN_OTHER = 50, 8, 5
N_IMAGES = 11
errs, warns = [], []


def sha1(path: Path) -> str:
    return hashlib.sha1(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()  # chuẩn hoá CRLF (Windows) -> LF


# 1. README
first = next((l for l in (ROOT / "README.md").read_text(encoding="utf-8").splitlines() if l.startswith("# ")), "")
if not re.match(r"# Day 13 Lab — .+: \S+ - .+", first):
    errs.append("dòng tiêu đề (dòng `# ...` đầu tiên) của README.md phải là: "
                "'# Day 13 Lab — <Họ và tên>: <MSHV> - <Họ và tên>' (xem SUBMISSION.md)")

# 2. mã số
student = ""
ini = configparser.ConfigParser()
ini.read(ROOT / "configs/lab.ini", encoding="utf-8-sig")  # Notepad/PowerShell có thể lưu kèm BOM
raw_student = ini.get("lab", "student", fallback="").strip()
if not raw_student:
    errs.append("configs/lab.ini chưa có `student` (mã số học viên)")
else:
    try:
        student = vf.normalize_student(raw_student)
    except SystemExit as exc:
        errs.append(f"configs/lab.ini: {exc}")
if ini.has_option("lab", "password") or ini.has_option("lab", "cvat_password"):
    errs.append("configs/lab.ini có mục mật khẩu: xoá ngay và đổi mật khẩu CVAT (RULES.md)")

# 3. file đã viết sẵn không được đổi
pin = ROOT / "scripts/_protected.json"
if pin.exists():
    for name, digest in json.loads(pin.read_text(encoding="utf-8")).items():
        if not (ROOT / name).exists() or sha1(ROOT / name) != digest:
            errs.append(f"{name} bị sửa so với bản đề (RULES.md: không sửa file đã viết sẵn)")
else:
    warns.append("thiếu scripts/_protected.json: không kiểm được file đã viết sẵn")

# 4. bảng A
rows, assigned = [], []
if student:
    task = vf.task_name(student)
    data = Path(ini.get("lab", "data", fallback="data/data-VF").strip() or "data/data-VF").expanduser()
    data = data if data.is_absolute() else ROOT / data
    try:
        counts = {seq: len(stamps) for seq, stamps in vf.list_sequences(data).items()}
    except SystemExit:
        counts = {seq: 60 for seq in range(1, 6)}
        warns.append(f"không thấy dữ liệu ở {data}: giả định 5 sequence × 60 frame để tính 10 frame của bạn")
    assigned = vf.select_frames(student, counts)
    print(f"mã số {student} · task {task} · frame: {', '.join(assigned)}")

    table = ROOT / "submission" / f"{task}-bangA.csv"
    if not table.exists():
        errs.append(f"thiếu submission/{table.name} (chạy `python scripts/lab.py report`)")
    else:
        with table.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            header = reader.fieldnames or []
            rows = list(reader)
        if header != TABLE_A_FIELDS:
            errs.append(f"{table.name}: cột khác bản do `report` sinh ra (bảng A bị sửa tay hoặc lưu lại từ Excel?)")
            rows = []
    if rows:
        if {r["student"] for r in rows} != {student}:
            errs.append(f"{table.name}: cột student không phải {student} (bảng A của người khác?)")
        bad_label = sorted({r["label"] for r in rows} - set(vf.CLASS_IDS))
        if bad_label:
            errs.append(f"{table.name}: class ngoài 5 class của guideline: {bad_label}")
        stray = sorted({r["frame"] for r in rows} - set(assigned))
        if stray:
            errs.append(f"{table.name}: có frame không thuộc 10 frame của mã số {student}: {stray}")
        per_frame = {name: sum(r["frame"] == name for r in rows) for name in assigned}
        print(f"bảng A: {len(rows)} cuboid · " + " ".join(f"{k}={v}" for k, v in per_frame.items()))
        if len(rows) < MIN_TOTAL:
            warns.append(f"tổng {len(rows)} cuboid < {MIN_TOTAL}: chưa đủ điều kiện đạt (RUBRIC.md)")
        for index, (name, count) in enumerate(per_frame.items()):
            need = MIN_FIRST if index == 0 else MIN_OTHER
            if count < need:
                warns.append(f"frame {name}: {count} cuboid < {need}")
        swapped = [f"{r['frame']}#{r['idx']}" for r in rows
                   if r["label"] != "Pedestrian" and float(r["length"]) < float(r["width"])]
        if swapped:
            warns.append(f"{len(swapped)} cuboid có length < width (mũi tên yaw nằm ngang thân xe?): {', '.join(swapped[:8])}")
    elif table.exists() and header == TABLE_A_FIELDS:
        errs.append(f"{table.name} trống: bấm Save trong CVAT rồi chạy lại `python scripts/lab.py report`")

    # 5. phiếu tự kiểm phải khớp bảng A
    check = ROOT / "submission" / f"{task}-tukiem.csv"
    if not check.exists():
        errs.append(f"thiếu submission/{check.name} (chạy `python scripts/lab.py selfcheck`)")
    elif rows:
        with check.open(encoding="utf-8-sig", newline="") as handle:
            checked = list(csv.DictReader(handle))
        if {(r["frame"], r["idx"]) for r in checked} != {(r["frame"], r["idx"]) for r in rows}:
            errs.append(f"{check.name} không khớp bảng A hiện tại: chạy lại `python scripts/lab.py selfcheck` sau `report`")
        else:
            flagged = sum(bool(r.get("flags")) for r in checked)
            print(f"tự kiểm: {flagged}/{len(checked)} cuboid còn cảnh báo (cảnh báo không tính điểm)")

# 6. báo cáo
report = ROOT / "submission/REPORT.md"
if not report.exists():
    errs.append("thiếu submission/REPORT.md")
else:
    text = report.read_text(encoding="utf-8")
    if "TODO(học viên)" in text:
        errs.append(f"submission/REPORT.md còn {text.count('TODO(học viên)')} dấu TODO(học viên) chưa điền")
    if student and student not in text.upper():
        errs.append(f"submission/REPORT.md không nhắc tới mã số {student}")
    missing = [name for name in assigned[:2] if name not in text]
    if assigned and missing:
        warns.append(f"REPORT.md mục 2 chưa nhắc tới hai frame đọc kỹ đầu tiên: {missing}")

# 7. ảnh chụp: nằm trên máy, nộp qua LMS, không vào git
images = [p for p in (ROOT / "submission/images").glob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg"}]
if len(images) < N_IMAGES:
    warns.append(f"submission/images có {len(images)}/{N_IMAGES} ảnh chụp (T1: 4, T2: 3, T4: 4); ảnh nộp qua LMS bằng `python scripts/lab.py pack`")

# 8. không commit dữ liệu
try:
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
except OSError:
    tracked = []
    warns.append("không chạy được git: không kiểm được file đã commit")
leaked = [f for f in tracked
          if (Path(f).suffix.lower() in {".bin", ".pcd", ".zip", ".jpg", ".jpeg", ".png"} and not f.startswith("docs/assets/"))
          or f.startswith(("data/data-VF/", "work/"))]
if leaked:
    errs.append(f"repo đang theo dõi {len(leaked)} file dữ liệu/ảnh (RULES.md: không commit dữ liệu VF): {leaked[:5]}")

print()
for w in warns:
    print("CẢNH BÁO:", w)
for e in errs:
    print("LỖI:", e)
print(f"\n{len(errs)} lỗi, {len(warns)} cảnh báo")
sys.exit(1 if errs else 0)
