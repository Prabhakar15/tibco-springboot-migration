"""Run the agent-based migration using LeaderAgent."""
import argparse
import logging
from pathlib import Path
from .leader import LeaderAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', required=True, help='Directory containing TIBCO BW artifacts')
    parser.add_argument('--output-dir', required=True, help='Output directory for generated projects')
    parser.add_argument('--package-root', default='com.example.tibco_migration', help='Java package root')
    args = parser.parse_args()
    
    leader = LeaderAgent(args.input_dir, args.output_dir, args.package_root)
    report = leader.execute()
    logger.info('Migration completed successfully')
    logger.info(f'Generated files: {len(report["generated_files"])}')
    logger.info(f'Created archives: {len(report["archives"])}')
    for arch in report['archives']:
        logger.info(f'Archive: {arch}')

if __name__ == '__main__':
    main()