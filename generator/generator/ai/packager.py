"""Packager: create zip archives for generated output folders."""
from pathlib import Path
import zipfile
import logging
from typing import List

logger = logging.getLogger(__name__)


class Packager:
    def _zip_folder(self, src: Path, dst: Path):
        with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in src.rglob('*'):
                if file.is_file():  # Only add files, not directories
                    # write the file with a relative path
                    zf.write(file, file.relative_to(src))
                    logger.info(f"Added {file.relative_to(src)} to {dst}")

    def package_output(self, output_base: str) -> List[str]:
        out = Path(output_base)
        archives = []
        if not out.exists():
            return archives
        # Instead of packaging the rest/soap folders generically, package per-process
        # Use the process name (folder name) as the base for archive names when possible.
        for child in out.iterdir():
            if not child.is_dir():
                continue
            # If child contains subfolders that are process outputs (e.g. LoanApp),
            # package each process subfolder. Otherwise, package the service folder
            # itself using a descriptive name.
            subdirs = [d for d in child.iterdir() if d.is_dir()]
            if subdirs:
                for sd in subdirs:
                    archive_path = out / f"{sd.name}_{child.name}.zip"
                    self._zip_folder(sd, archive_path)
                    archives.append(str(archive_path))
                    logger.info(f"Packaged {sd} -> {archive_path}")
            else:
                archive_path = out / f"{child.name}.zip"
                self._zip_folder(child, archive_path)
                archives.append(str(archive_path))
                logger.info(f"Packaged {child} -> {archive_path}")
        return archives
