from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_public_result_tables() -> None:
    root = Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, str(root / "scripts" / "check_public_results.py")],
        cwd=root,
        check=True,
    )
