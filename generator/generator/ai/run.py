"""Run the agent-based migration using LeaderAgent."""
import argparse
import logging
from pathlib import Path
from .leader import LeaderAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='TIBCO BusinessWorks to Spring Boot Migration')
    parser.add_argument('--input-dir', required=True, help='Directory containing TIBCO BW artifacts')
    parser.add_argument('--output-dir', required=True, help='Output directory for generated projects')
    parser.add_argument('--package-root', default='com.example.tibco_migration', help='Java package root')
    
    # Architecture selection
    parser.add_argument(
        '--architecture', 
        choices=['layered', 'hexagonal'], 
        default='layered',
        help='Architecture pattern: layered (default, separate REST/SOAP) or hexagonal (ports & adapters)'
    )
    
    # Service type for hexagonal architecture
    parser.add_argument(
        '--service-type',
        choices=['rest', 'soap', 'combined'],
        default='combined',
        help='Service type for hexagonal architecture: rest, soap, or combined (default)'
    )
    
    args = parser.parse_args()
    
    leader = LeaderAgent(
        args.input_dir, 
        args.output_dir, 
        args.package_root,
        architecture=args.architecture,
        service_type=args.service_type
    )
    report = leader.execute()
    logger.info('Migration completed successfully')
    logger.info(f'Architecture: {args.architecture}')
    if args.architecture == 'hexagonal':
        logger.info(f'Service type: {args.service_type}')
    logger.info(f'Generated files: {len(report["generated_files"])}')
    logger.info(f'Created archives: {len(report["archives"])}')
    for arch in report['archives']:
        logger.info(f'Archive: {arch}')

if __name__ == '__main__':
    main()