#!/usr/bin/env python3
"""Lệnh tắt của Lab Ngày 13 (ĐÃ VIẾT SẴN). Chạy giống nhau trên Windows, macOS, Linux.

    python scripts/lab.py dry         xem 10 frame của bạn, không nối CVAT
    python scripts/lab.py task        tạo task D13-<MÃ SỐ> trên CVAT
    python scripts/lab.py report      xuất bảng A  -> submission/D13-<MÃ SỐ>-bangA.csv
    python scripts/lab.py preview     vẽ cuboid lên ảnh camera -> work/xem/
    python scripts/lab.py selfcheck   soát cuboid bằng point cloud -> submission/D13-<MÃ SỐ>-tukiem.csv
    python scripts/lab.py sync        report + preview + selfcheck
    python scripts/lab.py pack        nén submission/images -> work/K5-L23-DAY13-<MÃ SỐ>-images.zip

Mã số, địa chỉ CVAT, tên đăng nhập và thư mục dữ liệu đọc từ configs/lab.ini.
Mật khẩu CVAT được hỏi khi chạy (hoặc lấy từ biến môi trường CVAT_PASSWORD); không ghi vào file nào.
"""
from __future__ import annotations

import argparse
import configparser
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cvat_lab"))

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}


def load_config() -> dict:
    """Đọc configs/lab.ini; dừng với thông báo rõ nếu chưa điền mã số."""
    path = ROOT / "configs" / "lab.ini"
    parser = configparser.ConfigParser()
    if not parser.read(path, encoding="utf-8") or "lab" not in parser:
        raise SystemExit(f"Không đọc được {path}. File phải có mục [lab].")
    cfg = {key: value.strip() for key, value in parser["lab"].items()}
    if not cfg.get("student"):
        raise SystemExit("Chưa điền `student` trong configs/lab.ini (mã số học viên của bạn).")
    cfg.setdefault("cvat_host", "http://localhost:8080")
    cfg.setdefault("data", "data/data-VF")
    return cfg


def data_dir(cfg: dict) -> Path:
    path = Path(cfg["data"]).expanduser()
    return path if path.is_absolute() else ROOT / path


def server_args(cfg: dict) -> list[str]:
    if not cfg.get("cvat_user"):
        raise SystemExit("Chưa điền `cvat_user` trong configs/lab.ini (tên đăng nhập CVAT).")
    args = ["--host", cfg["cvat_host"], "--user", cfg["cvat_user"]]
    if cfg.get("cvat_org"):
        args += ["--org", cfg["cvat_org"]]
    return args


def pack_images(student: str) -> int:
    """Nén ảnh chụp màn hình của báo cáo để nộp lên LMS (ảnh không đưa lên repo public)."""
    folder = ROOT / "submission" / "images"
    images = sorted(p for p in folder.glob("*") if p.suffix.lower() in IMAGE_SUFFIXES)
    if not images:
        raise SystemExit(f"Chưa có ảnh nào trong {folder}.")
    out = ROOT / "work" / f"K5-L23-DAY13-{student}-images.zip"
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for image in images:
            bundle.write(image, f"images/{image.name}")
    print(f"Đã nén {len(images)} ảnh -> {out}")
    print("Nộp file zip này lên LMS cùng link repo. Không commit ảnh.")
    return 0


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["dry", "task", "report", "preview", "selfcheck", "sync", "pack"])
    parser.add_argument("--replace", action="store_true",
                        help="chỉ cho `task`: XÓA task cùng tên và mọi cuboid rồi tạo lại")
    args = parser.parse_args(argv)

    import vf_common as vf
    import vf_cvat

    cfg = load_config()
    student = vf.normalize_student(cfg["student"])
    name = vf.task_name(student)
    table = ROOT / "submission" / f"{name}-bangA.csv"
    selfcheck = ROOT / "submission" / f"{name}-tukiem.csv"
    base = ["--student", student]
    data = ["--data", str(data_dir(cfg))]

    if args.command == "pack":
        return pack_images(student)
    if args.command == "dry":
        return vf_cvat.main(["day13", *base, *data, "--dry-run"])
    if args.command == "task":
        extra = ["--replace"] if args.replace else []
        return vf_cvat.main(["day13", *base, *data, *server_args(cfg), *extra])

    steps = ["report", "preview", "selfcheck"] if args.command == "sync" else [args.command]
    for step in steps:
        if step == "report":
            code = vf_cvat.main(["report", "d13", *base, *server_args(cfg), "--out", str(table.parent)])
        elif step == "preview":
            code = vf_cvat.main(["preview", "d13", *base, *data, "--table", str(table), "--out", str(ROOT / "work" / "xem")])
        else:
            code = vf_cvat.main(["check", "d13", *base, *data, "--table", str(table), "--out", str(selfcheck)])
        if code:
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
