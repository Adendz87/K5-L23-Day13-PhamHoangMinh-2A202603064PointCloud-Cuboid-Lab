#!/usr/bin/env python3
"""Tự kiểm tra bài nộp trước khi push (ĐÃ VIẾT SẴN). `python scripts/check_submission.py` — hết LỖI mới nộp.

Script chỉ kiểm bài nộp có ĐỦ và NHẤT QUÁN không. Nó không biết đáp án và không chấm cuboid của bạn đúng hay sai.
"""
from __future__ import annotations

import configparser
import csv
import hashlib
import io
import json
import math
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cvat_lab"))
sys.path.insert(0, str(ROOT / "scripts"))
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

import vf_common as vf  # noqa: E402
from lab import IMAGE_SUFFIXES, N_IMAGES, data_dir, load_config  # noqa: E402
from vf_cvat import TABLE_A_FIELDS  # noqa: E402
from vf_qa import CHECK_FIELDS  # noqa: E402

MIN_TOTAL, MIN_FIRST, MIN_OTHER = 50, 8, 5
BOM = b"\xef\xbb\xbf"
INI_KEYS = {"student", "cvat_host", "cvat_user", "cvat_org", "data"}
SECRET_KEY = re.compile(r"pass|pwd|mat_?khau|mật|token|secret", re.IGNORECASE)
# File không bao giờ được vào repo public: dữ liệu VF, ảnh, file nén, video, tài liệu xuất, bảng điểm.
# Riêng bảng A và phiếu tự kiểm của bạn (submission/D13-<MÃ SỐ>-bangA.csv, -tukiem.csv) phải được commit.
LEAK_SUFFIXES = {".bin", ".pcd", ".ply", ".zip", ".7z", ".rar", ".tar", ".gz", ".tgz", ".jpg", ".jpeg", ".png",
                 ".webp", ".heic", ".gif", ".bmp", ".tif", ".tiff", ".mp4", ".mov", ".pdf", ".docx", ".pptx", ".csv"}
LEAK_PART = re.compile(r"sequence_\d+|data-vf|calib\.json|hoso|.*-hoso\.md", re.IGNORECASE)
ALLOWED = {"docs/assets/hero.png", "docs/assets/coordinates.png", "docs/assets/workflow.png",
           "docs/3D_Cuboid_Annotation_Guideline.docx"}
SUBMITTED_CSV = re.compile(r"submission/D13-([^/]+)-(?:bangA|tukiem)\.csv")
# Định dạng đúng như `report` ghi ra (cvat_lab/vf_cvat.py, table_a_row). Excel lưu lại sẽ làm sai định dạng.
FORMATS = {key: re.compile(pattern) for key, pattern in {
    "frame": r"s\d{2}f\d{2}", "idx": r"[1-9]\d*", "occluded": r"[01]",
    **{k: r"-?\d+\.\d{3}" for k in ("x", "y", "z", "length", "width", "height", "z_bottom")},
    "yaw_rad": r"-?\d+\.\d{4}", "yaw_deg": r"-?\d+\.\d", "az_deg": r"-?\d+\.\d", "dist_m": r"\d+\.\d{2}",
    "dist_bin": r"0-10|10-20|20-30|30-50|>=50",
}.items()}
errs, warns = [], []


def sha1(path: Path) -> str:
    return hashlib.sha1(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()  # chuẩn hoá CRLF (Windows) -> LF


def git(*args: str) -> str | None:
    """Chạy git, trả về stdout (UTF-8), hoặc None nếu không có git / không phải git repo."""
    try:
        result = subprocess.run(["git", "-c", "core.quotepath=off", *args], cwd=ROOT, capture_output=True)
    except OSError:
        return None
    return result.stdout.decode("utf-8", errors="replace") if result.returncode == 0 else None


def leaks(paths) -> list[str]:
    found = []
    for path in paths:
        low = path.lower()
        parts = low.split("/")
        if path in ALLOWED or low in ("data/readme.md",) or SUBMITTED_CSV.fullmatch(path):
            continue
        if (Path(low).suffix in LEAK_SUFFIXES or parts[0] in {"data", "work", "nop", "xem"}
                or any(LEAK_PART.fullmatch(part) for part in parts)):
            found.append(path)
    return found


def row_problem(row: dict, student: str) -> str | None:
    """Lý do một dòng bảng A không giống bản `report` sinh ra, hoặc None."""
    if row.get("student") != student:
        return f"student = {row.get('student')!r}"
    if row.get("label") not in vf.CLASS_IDS:
        return f"class {row.get('label')!r} ngoài 5 class"
    for key, pattern in FORMATS.items():
        if not pattern.fullmatch(row.get(key) or ""):
            return f"{key} = {row.get(key)!r} sai định dạng"
    x, y, z, height, yaw_rad, yaw_deg, z_bottom, dist, az = (float(row[k]) for k in (
        "x", "y", "z", "height", "yaw_rad", "yaw_deg", "z_bottom", "dist_m", "az_deg"))
    if abs(z_bottom - (z - height / 2)) > 0.002:
        return "z_bottom khác z − height/2"
    if abs(dist - math.hypot(x, y)) > 0.006:
        return "dist_m khác √(x² + y²)"
    if abs(yaw_deg - math.degrees(yaw_rad)) > 0.06:
        return "yaw_deg khác yaw_rad"
    expected = vf.azimuth_deg({"x": x, "y": y})
    if abs((az - expected + 180) % 360 - 180) > 0.051 + math.degrees(0.0008 / max(dist, 1e-3)):
        return "az_deg khác góc của tâm"
    if row["dist_bin"] not in {vf.dist_bin(dist - 0.005), vf.dist_bin(dist + 0.005)}:
        return "dist_bin khác dist_m"
    return None


# 1. cấu hình
cfg, student = {}, ""
try:
    cfg = load_config(require_student=False)
except SystemExit as exc:
    errs.append(f"configs/lab.ini: {exc}")
if cfg and not cfg.get("student"):
    errs.append("configs/lab.ini chưa có `student` (mã số học viên)")
elif cfg:
    try:
        student = vf.normalize_student(cfg["student"])
    except SystemExit as exc:
        errs.append(f"configs/lab.ini: {exc}")
ini = configparser.ConfigParser(interpolation=None, inline_comment_prefixes=("#", ";"), strict=False)
try:
    ini.read(ROOT / "configs/lab.ini", encoding="utf-8-sig")
except (configparser.Error, UnicodeDecodeError):
    pass  # đã báo ở trên
for section in ini.sections():
    for key, value in ini[section].items():
        if SECRET_KEY.search(key) and value.strip():
            errs.append(f"configs/lab.ini có khoá `{key}` giống mật khẩu: xoá ngay, đổi mật khẩu CVAT (RULES.md)")
        elif section == "lab" and key not in INI_KEYS:
            warns.append(f"configs/lab.ini có khoá lạ `{key}` (chỉ cần {', '.join(sorted(INI_KEYS))})")
    if section != "lab":
        warns.append(f"configs/lab.ini có mục lạ [{section}]")

# 2. README
first = next((l for l in (ROOT / "README.md").read_text(encoding="utf-8").splitlines() if l.startswith("# ")), "")
title = re.match(r"# Day 13 Lab\s*[—–-]\s*(.+?):\s*(\S+)\s+-\s+(.+)$", first)
if not title or "<" in first or ">" in first:
    errs.append("dòng tiêu đề (dòng `# ...` đầu tiên) của README.md phải là: "
                "'# Day 13 Lab — <Họ và tên>: <MSHV> - <Họ và tên>', thay cả dấu < > (xem SUBMISSION.md)")
elif student and title.group(2).strip().upper() != student:
    errs.append(f"README.md: MSHV ở dòng tiêu đề ({title.group(2)}) khác `student` trong configs/lab.ini ({student})")

# 3. file đã viết sẵn không được đổi
pin = ROOT / "scripts/_protected.json"
if pin.exists():
    for name, digest in json.loads(pin.read_text(encoding="utf-8")).items():
        if not (ROOT / name).exists() or sha1(ROOT / name) != digest:
            errs.append(f"{name} bị sửa so với bản đề (RULES.md: không sửa file đã viết sẵn)")
else:
    warns.append("thiếu scripts/_protected.json: không kiểm được file đã viết sẵn")

# 4. bảng A
rows, assigned, header = [], [], []
table = check = None
if student:
    task = vf.task_name(student)
    data = data_dir(cfg)
    try:
        counts = {seq: len(stamps) for seq, stamps in vf.list_sequences(data).items()}
    except SystemExit:
        counts = {seq: 60 for seq in range(1, 6)}
        warns.append(f"không thấy dữ liệu ở {data}: giả định 5 sequence × 60 frame để tính 10 frame của bạn")
    assigned = vf.select_frames(student, counts)
    print(f"mã số {student} · task {task} · frame: {', '.join(assigned)}")

    table = ROOT / "submission" / f"{task}-bangA.csv"
    if not table.exists():
        errs.append(f"thiếu submission/{table.name}: bấm Save trong CVAT rồi chạy `python scripts/lab.py sync`")
    else:
        raw = table.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = None
        if raw.startswith(BOM) or text is None:
            errs.append(f"{table.name} đã bị lưu lại bằng bảng tính (BOM/bảng mã khác): công cụ chấm không đọc được. "
                        "Chạy lại `python scripts/lab.py sync`")
        else:
            reader = csv.DictReader(io.StringIO(text, newline=""))
            header = reader.fieldnames or []
            rows = list(reader)
            if header != TABLE_A_FIELDS:
                errs.append(f"{table.name}: cột khác bản do `report` sinh ra (sửa tay hoặc lưu lại từ Excel?). "
                            "Chạy lại `python scripts/lab.py sync`")
                rows = []
            elif not rows:
                errs.append(f"{table.name} trống: bấm Save trong CVAT (vẽ bằng Shape, không phải Track) rồi chạy lại "
                            "`python scripts/lab.py sync`")
    if rows:
        problems = [f"dòng {n}: {why}" for n, row in enumerate(rows, start=2) if (why := row_problem(row, student))]
        keys = [(r["frame"], r["idx"]) for r in rows]
        if len(set(keys)) != len(keys):
            problems.append("có cặp (frame, idx) lặp lại")
        if problems:
            errs.append(f"{table.name} không giống bản do `report` sinh ra ({len(problems)} chỗ, ví dụ "
                        f"{'; '.join(problems[:3])}): đừng sửa tay hay lưu lại từ Excel. Chạy lại `python scripts/lab.py sync`")
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
        if not problems:
            swapped = [f"{r['frame']}#{r['idx']}" for r in rows
                       if r["label"] != "Pedestrian" and float(r["length"]) < float(r["width"])]
            if swapped:
                warns.append(f"{len(swapped)} cuboid có length < width (mũi tên yaw nằm ngang thân xe?): "
                             f"{', '.join(swapped[:8])}")

    # 5. phiếu tự kiểm phải khớp bảng A hiện tại
    check = ROOT / "submission" / f"{task}-tukiem.csv"
    if not check.exists():
        errs.append(f"thiếu submission/{check.name} (chạy `python scripts/lab.py selfcheck` hoặc `sync`)")
    elif rows:
        stale = True
        try:
            with check.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                checked = list(reader)
            if reader.fieldnames == CHECK_FIELDS:
                mine = {(r["frame"], r["idx"]): (r["label"], math.hypot(float(r["x"]), float(r["y"]))) for r in rows}
                theirs = {(r["frame"], r["idx"]): (r["label"], float(r["dist_m"])) for r in checked}
                stale = mine.keys() != theirs.keys() or any(
                    theirs[k][0] != mine[k][0] or abs(theirs[k][1] - mine[k][1]) > 0.06 for k in mine)
        except (UnicodeDecodeError, ValueError, KeyError, csv.Error):
            stale = True
        if stale:
            errs.append(f"{check.name} không khớp bảng A hiện tại (cũ hơn, hoặc bị sửa): chạy lại `python scripts/lab.py sync`")
        else:
            flagged = sum(bool(r.get("flags")) for r in checked)
            print(f"tự kiểm: {flagged}/{len(checked)} cuboid còn cảnh báo (cảnh báo không tính điểm)")

# 6. báo cáo
report = ROOT / "submission/REPORT.md"
if not report.exists():
    errs.append("thiếu submission/REPORT.md")
else:
    text = report.read_text(encoding="utf-8")
    todo = sum(line.count("TODO(học viên)") for line in text.splitlines() if not line.lstrip().startswith(">"))
    if todo:
        errs.append(f"submission/REPORT.md còn {todo} dấu TODO(học viên) chưa điền")
    if "<Họ và tên>" in text or "<MSHV>" in text:
        errs.append("submission/REPORT.md: dòng đầu còn <Họ và tên> hoặc <MSHV>")
    if student and student not in text.upper():
        errs.append(f"submission/REPORT.md không nhắc tới mã số {student}")
    missing = [name for name in assigned[:2] if name not in text]
    if assigned and missing:
        warns.append(f"REPORT.md mục 2 chưa nhắc tới hai frame đọc kỹ đầu tiên: {missing}")

# 7. ảnh chụp: nằm trên máy, nộp qua LMS trong file zip, không vào git
images = [p for p in (ROOT / "submission/images").glob("*") if p.suffix.lower() in IMAGE_SUFFIXES]
if len(images) < N_IMAGES:
    warns.append(f"submission/images có {len(images)}/{N_IMAGES} ảnh chụp (Bước 2: 4, Bước 3: 3, Bước 4: 4)")
if student and images:
    bundle = ROOT / "work" / f"K5-L23-DAY13-{student}-images.zip"
    try:
        with zipfile.ZipFile(bundle) as archive:
            zipped = {n for n in archive.namelist() if n.startswith("images/") and not n.endswith("/")}
    except (OSError, zipfile.BadZipFile):
        zipped = None
    if zipped is None:
        warns.append(f"chưa có work/{bundle.name} (ảnh nộp LMS): chạy `python scripts/lab.py pack`")
    elif zipped != {f"images/{p.name}" for p in images}:
        warns.append(f"work/{bundle.name} khác ảnh trong submission/images: chạy lại `python scripts/lab.py pack`")

# 8. repo public: không commit dữ liệu, ảnh; bảng A, phiếu tự kiểm, báo cáo đã commit và push chưa
listing = git("ls-files", "-z")
if listing is None:
    warns.append("thư mục này không phải git repo (tải ZIP?) hoặc không chạy được git: không kiểm được file sẽ push. "
                 "Hãy `git clone` repo của bạn và nộp bằng git")
else:
    tracked = [f for f in listing.split("\0") if f]
    leaked = leaks(tracked)
    if leaked:
        errs.append(f"repo đang theo dõi {len(leaked)} file không được đưa lên repo public (dữ liệu, ảnh, file nén): "
                    f"{leaked[:5]}. Gỡ: `git rm --cached <file>` (docs/COMMON_ERRORS.md mục 5)")
    others = sorted(f for f in tracked if (m := SUBMITTED_CSV.fullmatch(f)) and m.group(1).upper() != student)
    if student and others:
        errs.append(f"repo có bảng A hoặc phiếu tự kiểm của mã số khác: {others[:4]}. Chỉ commit file của mã {student}")
    history = git("log", "--all", "--format=", "--name-only", "--diff-filter=A", "-z") or ""
    old_leaks = sorted(set(leaks(f for f in history.split("\0") if f.strip())) - set(leaked))
    if old_leaks:
        errs.append(f"lịch sử commit vẫn còn {len(old_leaks)} file không được public: {old_leaks[:5]}. "
                    "Gỡ khỏi git chưa đủ: xem docs/COMMON_ERRORS.md mục 5 trước khi push")
    paths = ["README.md", "submission/REPORT.md", "configs/lab.ini"]
    if student:
        paths += [f"submission/D13-{student}-bangA.csv", f"submission/D13-{student}-tukiem.csv"]
    dirty = git("status", "--porcelain", "--untracked-files=all", "--", *paths)
    if dirty and dirty.strip():
        changed = sorted({line[3:].strip().strip('"') for line in dirty.splitlines() if len(line) > 3})
        warns.append(f"chưa commit: {', '.join(changed)}. Coach chấm từ repo: chạy `git add -A`, `git commit`, `git push`")
    ahead = git("rev-list", "--count", "@{u}..HEAD")
    if ahead and ahead.strip() not in ("", "0"):
        warns.append(f"có {ahead.strip()} commit chưa push: chạy `git push`")

print()
for w in warns:
    print("CẢNH BÁO:", w)
for e in errs:
    print("LỖI:", e)
print(f"\n{len(errs)} lỗi, {len(warns)} cảnh báo")
sys.exit(1 if errs else 0)
