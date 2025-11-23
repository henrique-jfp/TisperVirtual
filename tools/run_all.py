"""Launcher to start backend, frontend and Streamlit from the project venv.

Use this when you prefer a single terminal that spawns all processes and
collects logs under `logs/`.

Run: python tools/run_all.py
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class ProcessSpec:
    name: str
    cmd: List[str]
    cwd: Path
    logfile: Path


def make_specs(root: Path) -> List[ProcessSpec]:
    logs = root / "logs"
    logs.mkdir(exist_ok=True)

    py = sys.executable
    return [
        ProcessSpec(
            name="backend",
            cmd=[py, "-m", "uvicorn", "api_server:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=root,
            logfile=logs / "backend.log",
        ),
        ProcessSpec(
            name="streamlit",
            cmd=[py, "-m", "streamlit", "run", "tipster_app.py"],
            cwd=root,
            logfile=logs / "streamlit.log",
        ),
        ProcessSpec(
            name="frontend",
            # On Windows it's more reliable to run npm through cmd.exe
            cmd=["cmd.exe", "/c", "npm", "run", "dev"],
            cwd=root / "frontend",
            logfile=logs / "frontend.log",
        ),
    ]


def start_process(spec: ProcessSpec) -> subprocess.Popen:
    print(f"Starting {spec.name}: {' '.join(spec.cmd)} (cwd={spec.cwd})")
    logfile = spec.logfile.open("ab")
    proc = subprocess.Popen(
        spec.cmd,
        cwd=str(spec.cwd),
        stdout=logfile,
        stderr=subprocess.STDOUT,
        shell=False,
    )
    return proc


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    specs = make_specs(root)

    procs = []
    try:
        for s in specs:
            p = start_process(s)
            procs.append((s, p))

        print("All processes started. Logs are in %s" % (root / "logs"))
        print("Press Ctrl+C to terminate all processes.")

        # wait until interrupted
        for _, p in procs:
            p.wait()

    except KeyboardInterrupt:
        print("Interrupted — terminating children...")
        for spec, p in procs:
            if p.poll() is None:
                print(f"Terminating {spec.name} (pid={p.pid})")
                p.terminate()
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
