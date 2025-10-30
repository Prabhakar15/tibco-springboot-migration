"""Main entry point for AI-enhanced TIBCO migration."""

import os
from typing import Dict, Any
from .agents import MigrationOrchestrator
import logging

logger = logging.getLogger(__name__)

def migrate_process(
    process_file: str,
    output_dir: str,
    package_name: str,
    **options: Dict[str, Any]
) -> bool:
    """
    Migrate a TIBCO process to Spring Boot using AI-enhanced tools.
    
    Args:
        process_file: Path to the TIBCO process file
        output_dir: Directory to store generated files
        package_name: Java package name for generated code
        options: Additional migration options
        
    Returns:
        bool: True if migration was successful, False otherwise
    """
    try:
        # Create orchestrator
        orchestrator = MigrationOrchestrator(
            process_file=process_file,
            output_dir=output_dir,
            package_name=package_name
        )
        
        # Execute migration
        success = orchestrator.execute_migration()
        
        if success:
            logger.info("Migration completed successfully")
        else:
            logger.error("Migration failed - check migration_report.json for details")
        
        return success
        
    except Exception as e:
        logger.error(f"Migration failed with error: {str(e)}")
        return False