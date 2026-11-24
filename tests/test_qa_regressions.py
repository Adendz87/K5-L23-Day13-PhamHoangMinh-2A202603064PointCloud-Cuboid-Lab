import contextlib
import csv
import io
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
from argparse import Namespace
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import lab
import vf_common as vf
import vf_cvat

STUDENT = "QA13"


class TaskAndDataTests(unittest.TestCase):
    def test_existing_task_without_jobs_is_an_error(self):
        args = Namespace(student=STUDENT, data="unused", bundle_out=None, dry_run=False,
                         host="http://localhost:8080", user="tester", org=None, replace=False)
        task = Mock(id=123)
        task.get_jobs.return_value = []

        def build_stub(_frames, path):
            path.write_bytes(b"bundle")

        with (patch.object(vf_cvat, "frame_sources", return_value=[{"name": "s01f00", "seq": 1, "stamp": "0", "cameras": []}]),
              patch.object(vf_cvat, "build_bundle", side_effect=build_stub),
              patch.object(vf_cvat, "connect"), patch.object(vf_cvat, "find_tasks", return_value=[task]),
              contextlib.redirect_stdout(io.StringIO()),
              self.assertRaisesRegex(SystemExit, "chưa có job")):
            vf_cvat.cmd_day13(args)
        task.remove.assert_not_called()

    def test_missing_sequence_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            data = Path(folder)
            for seq in range(1, 5):
                path = data / f"sequence_{seq:02d}"
                (path / "lidar").mkdir(parents=True)
                (path / "calib.json").write_text(
                    '{"calib":{"cam01":{"cam_to_velo":[[],[0,0,-1]]}}}', encoding="utf-8")
                for frame in range(60):
                    (path / "lidar" / f"{frame:03d}.bin").write_bytes(struct.pack("<4f", 1, 0, 0, 0))
            with self.assertRaisesRegex(SystemExit, "sequence_05"):
                lab.check_data(data)


class CheckerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for folder in ("scripts", "cvat_lab"):
            shutil.copytree(ROOT / folder, self.root / folder, ignore=shutil.ignore_patterns("__pycache__"))
        (self.root / "configs").mkdir()
        (self.root / "configs/lab.ini").write_text(f"[lab]\nstudent = {STUDENT}\n", encoding="utf-8")
        (self.root / "README.md").write_text(f"# Day 13 Lab - Test User: {STUDENT} - Test User\n", encoding="utf-8")

        frames = vf.select_frames(STUDENT, dict.fromkeys(range(1, 6), 60))
        report_dir = self.root / "report/individual"
        (report_dir / "images").mkdir(parents=True)
        (report_dir / f"{STUDENT}_TestUser.md").write_text(f"# {STUDENT}\n{frames[0]} {frames[1]}\n", encoding="utf-8")
        box = {"x": 1, "y": -10, "z": -1, "length": 4, "width": 2, "height": 1.5, "yaw": 4.7, "label": "Car"}
        self.table = self.root / "submission" / f"D13-{STUDENT}-bangA.csv"
        vf_cvat.write_table_a(self.table, STUDENT, [vf_cvat.table_a_row(frames[0], 1, box)])

        data = self.root / "data/data-VF"
        for frame in frames:
            seq, idx = vf.parse_frame_name(frame)
            lidar = data / f"sequence_{seq:02d}" / "lidar"
            lidar.mkdir(parents=True, exist_ok=True)
            for n in range(60):
                (lidar / f"{n:03d}.bin").write_bytes(struct.pack("<4f", 1, -10, -1, 0))
        self.probe = self.root / "submission" / f"D13-{STUDENT}-tukiem.csv"
        result = self.run_python("cvat_lab/vf_cvat.py", "check", "d13", "--student", STUDENT,
                                 "--data", str(data), "--table", str(self.table), "--out", str(self.probe))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

        self.images = [f"t1-{frame}-{view}.png" for frame in frames[:2] for view in ("3d", "top")]
        self.images += ["t2-a-car.png", "t2-b-bus-truck.png", "t2-c-ped-cyclist.png", "t4-1-bong-che.png",
                        "t4-2-thua-o-xa.png", "t4-3-phan-xa-thap.png", "t4-4-diem-la.png"]
        for name in self.images:
            (report_dir / "images" / name).write_bytes(b"synthetic image fixture")
        self.bundle = self.root / "work" / f"K5-L23-DAY13-{STUDENT}-images.zip"
        self.bundle.parent.mkdir()
        with zipfile.ZipFile(self.bundle, "w") as archive:
            for name in self.images:
                archive.write(report_dir / "images" / name, f"images/{name}")

    def run_python(self, *args):
        return subprocess.run([sys.executable, *args], cwd=self.root, capture_output=True, encoding="utf-8")

    def check(self):
        return self.run_python("scripts/check_submission.py")

    def test_valid_outputs_pass(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_missing_zip_blocks_submission(self):
        self.bundle.unlink()
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("LỖI: chưa có work/", result.stdout)

    def test_corrupt_zip_payload_blocks_submission(self):
        with zipfile.ZipFile(self.bundle) as archive:
            start = archive.infolist()[0].header_offset
        content = bytearray(self.bundle.read_bytes())
        name_length, extra_length = struct.unpack_from("<HH", content, start + 26)
        content[start + 30 + name_length + extra_length] ^= 0xFF
        self.bundle.write_bytes(content)
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("bị hỏng", result.stdout)

    def test_zip_missing_a_required_view_blocks_submission(self):
        with zipfile.ZipFile(self.bundle, "w") as archive:
            for name in self.images[1:]:
                archive.writestr(f"images/{name}", b"synthetic image fixture")
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(self.images[0].removesuffix(".png"), result.stdout)

    def test_zip_with_duplicate_image_names_is_rejected(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.bundle, "a") as archive:
                archive.writestr(f"images/{self.images[0]}", b"synthetic image fixture")
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("bị hỏng", result.stdout)

    def test_truncated_csv_has_line_number_and_no_traceback(self):
        with self.table.open("ab") as handle:
            handle.write(f"\r\n{STUDENT}\r\n".encode())
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("dòng 4", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_geometry_change_invalidates_self_check(self):
        with self.table.open(newline="", encoding="utf-8") as handle:
            row, = csv.DictReader(handle)
        row["length"] = "7.500"
        with self.table.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=vf_cvat.TABLE_A_FIELDS)
            writer.writeheader()
            writer.writerow(row)
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("không khớp bảng A", result.stdout)


if __name__ == "__main__":
    unittest.main()
