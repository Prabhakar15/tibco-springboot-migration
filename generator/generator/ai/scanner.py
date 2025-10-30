"""Utilities to scan input directories for BW process folders."""
from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)


def find_bw_folders(base_dir: str) -> List[Path]:
    base = Path(base_dir)
    if not base.exists() or not base.is_dir():
        raise FileNotFoundError(base_dir)

    folders = []
    for child in base.iterdir():
        if not child.is_dir():
            continue
        if any(child.glob('*.process')) or any(child.glob('*.bwp')) or any(child.glob('*.xsd')):
            folders.append(child)
    logger.info(f"Found {len(folders)} BW folders under {base_dir}")
    return folders
