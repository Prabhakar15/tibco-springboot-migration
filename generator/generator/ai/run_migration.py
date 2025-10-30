"""Simple runner script to invoke LeaderAgent for AI-enhanced migration.

This module is intended to be used by developer/CI to run a migration of a base
input folder containing many BW process subfolders. It writes generated files
into the specified output_base and returns a JSON-like report structure.
"""
import argparse
import logging
from pathlib import Path
import json

from .leader import LeaderAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Run AI-enhanced BW -> Spring migration')
    parser.add_argument('--input', '-i', required=True, help='Input base folder containing BW folders')
    parser.add_argument('--output', '-o', required=True, help='Output base folder for generated code')
    parser.add_argument('--package', '-p', required=False, default='com.generated', help='Root Java package for generated code')

    args = parser.parse_args()
    leader = LeaderAgent(args.input, args.output, args.package)
    report = leader.execute()

    # persist report
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    report_file = out / 'ai_migration_report.json'
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    logger.info(f"Migration completed. Report written to {report_file}")


if __name__ == '__main__':
    main()
