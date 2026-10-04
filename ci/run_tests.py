"""Run assigned pytest node IDs against the installed distribution."""

import argparse
import json
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jobs", type=Path)
    parser.add_argument("--results", type=Path, default=Path("/results"))
    args = parser.parse_args()
    jobs = json.loads(args.jobs.read_text(encoding="utf-8"))
    results = args.results
    results.mkdir(parents=True, exist_ok=True)
    (results / "pyvcs-version.txt").write_text(version("pyvcs") + "\n", encoding="utf-8")
    failed = False
    for job in jobs:
        name = f"run-{job['id']:04d}"
        command = [
            sys.executable,
            "-m",
            "pytest",
            "--import-mode=importlib",
            "-v",
            f"--junitxml={results / (name + '.xml')}",
            f"--junit-prefix={name}",
            "--",
            job["nodeid"],
        ]
        print(f"Running {name}: {job['nodeid']}", flush=True)
        with (results / (name + ".log")).open("w", encoding="utf-8") as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
        print((results / (name + ".log")).read_text(encoding="utf-8"), flush=True)
        failed = failed or result.returncode != 0
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
