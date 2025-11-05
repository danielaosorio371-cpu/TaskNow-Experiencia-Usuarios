import argparse
import shutil
import subprocess
import sys

#!/usr/bin/env python3
# tu_archivo.py - small helper to run `git add` from Python


def check_git_available():
    if not shutil.which("git"):
        print("git not found on PATH.", file=sys.stderr)
        sys.exit(2)

def inside_git_repo():
    p = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                       capture_output=True, text=True)
    return p.returncode == 0

def run_git_add(paths, dry_run=False, verbose=False):
    cmd = ["git", "add"]
    if dry_run:
        cmd.append("--dry-run")
    cmd.extend(paths)
    if verbose:
        print("Running:", " ".join(cmd))
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.stdout:
        print(p.stdout, end="")
    if p.stderr:
        print(p.stderr, file=sys.stderr, end="")
    return p.returncode

def main():
    parser = argparse.ArgumentParser(description="Run `git add` (wrapper).")
    parser.add_argument("paths", nargs="*", default=["."], help="paths to add (default: .)")
    parser.add_argument("-n", "--dry-run", action="store_true", help="show what would be added")
    parser.add_argument("-v", "--verbose", action="store_true", help="print the git command")
    args = parser.parse_args()

    check_git_available()
    if not inside_git_repo():
        print("Not inside a git repository.", file=sys.stderr)
        sys.exit(1)

    rc = run_git_add(args.paths, dry_run=args.dry_run, verbose=args.verbose)
    sys.exit(rc)

if __name__ == "__main__":
    main()