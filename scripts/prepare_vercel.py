"""Remove dependency test suites from the Vercel runtime bundle."""

import os
from pathlib import Path
import shutil
import sysconfig


def main():
    if os.environ.get("VERCEL") != "1":
        raise RuntimeError("This packaging step is only for Vercel builds")

    site_packages = Path(sysconfig.get_path("purelib")).resolve()
    removed_bytes = 0
    for name in ("numpy", "pandas", "scipy", "sklearn"):
        package = site_packages / name
        for candidate in sorted(package.rglob("tests")):
            if not candidate.is_dir() or candidate.is_symlink():
                continue
            target = candidate.resolve()
            if not target.is_relative_to(package.resolve()):
                raise RuntimeError(f"Test directory escapes package: {target}")
            removed_bytes += sum(p.stat().st_size for p in target.rglob("*") if p.is_file())
            shutil.rmtree(target)
    print(f"Removed {removed_bytes / 1024**2:.1f} MiB of dependency tests")


if __name__ == "__main__":
    main()
