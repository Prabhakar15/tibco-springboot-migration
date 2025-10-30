"""Agent-based architecture for TIBCO to Spring Boot migration."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import logging
from .rag import ProcessKnowledgeBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MigrationContext:
    """Shared context between agents."""
    process_file: str
    output_dir: str
    package_name: str
    knowledge_base: ProcessKnowledgeBase
    generated_files: Dict[str, str] = None
    current_stage: str = "init"
    errors: List[str] = None
    warnings: List[str] = None

    def __post_init__(self):
        self.generated_files = {}
        self.errors = []
        self.warnings = []

class MigrationAgent(ABC):
    """Base class for all migration agents."""
    
    def __init__(self, context: MigrationContext):
        self.context = context
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def process(self) -> bool:
        """Process the migration task."""
        pass

    def add_warning(self, message: str):
        """Add a warning message to the context."""
        self.logger.warning(message)
        self.context.warnings.append(message)

    def add_error(self, message: str):
        """Add an error message to the context."""
        self.logger.error(message)
        self.context.errors.append(message)

class ProcessAnalyzerAgent(MigrationAgent):
    """Analyzes TIBCO process structure and activities."""
    
    def process(self) -> bool:
        try:
            self.context.current_stage = "process_analysis"
            self.context.knowledge_base.index_process_activities(self.context.process_file)
            
            # Analyze SQL activities
            sql_activities = self.context.knowledge_base.query_similar_activities(
                "SQL database operation", k=10
            )
            
            # Analyze JMS activities
            jms_activities = self.context.knowledge_base.query_similar_activities(
                "JMS messaging operation", k=10
            )
            
            # Store analysis results in context
            self.context.analysis_results = {
                'sql_activities': sql_activities,
                'jms_activities': jms_activities
            }
            
            return True
        except Exception as e:
            self.add_error(f"Process analysis failed: {str(e)}")
            return False

class CodeGeneratorAgent(MigrationAgent):
    """Generates Spring Boot code based on process analysis."""
    
    def process(self) -> bool:
        try:
            self.context.current_stage = "code_generation"
            
            # Generate JPA entities
            self._generate_jpa_entities()
            
            # Generate JMS configurations
            self._generate_jms_config()
            
            # Generate service layer
            self._generate_services()
            
            return True
        except Exception as e:
            self.add_error(f"Code generation failed: {str(e)}")
            return False

    def _generate_jpa_entities(self):
        """Generate JPA entities from SQL activities."""
        analysis = self.context.analysis_results['sql_activities']
        for activity in analysis:
            if activity['similarity_score'] > 0.8:  # High confidence match
                # Generate entity class
                entity_name = self._derive_entity_name(activity)
                entity_content = self._generate_entity_class(activity)
                
                file_path = f"{self.context.output_dir}/entity/{entity_name}.java"
                self.context.generated_files[file_path] = entity_content

    def _generate_jms_config(self):
        """Generate JMS configuration from JMS activities."""
        analysis = self.context.analysis_results['jms_activities']
        if analysis:
            config_content = self._generate_jms_configuration(analysis)
            file_path = f"{self.context.output_dir}/config/JmsConfig.java"
            self.context.generated_files[file_path] = config_content

class ConfigurationAgent(MigrationAgent):
    """Manages configuration files and dependencies."""
    
    def process(self) -> bool:
        try:
            self.context.current_stage = "configuration"
            
            # Generate application.yml
            self._generate_application_yml()
            
            # Generate pom.xml
            self._generate_pom_xml()
            
            return True
        except Exception as e:
            self.add_error(f"Configuration generation failed: {str(e)}")
            return False

    def _generate_application_yml(self):
        """Generate Spring Boot application.yml with proper configurations."""
        config_content = self._create_application_config()
        file_path = f"{self.context.output_dir}/resources/application.yml"
        self.context.generated_files[file_path] = config_content

class ValidationAgent(MigrationAgent):
    """Validates generated code and configurations."""
    
    def process(self) -> bool:
        try:
            self.context.current_stage = "validation"
            
            # Validate Java syntax
            self._validate_java_syntax()
            
            # Validate configurations
            self._validate_configurations()
            
            # Check dependencies
            self._validate_dependencies()
            
            return True
        except Exception as e:
            self.add_error(f"Validation failed: {str(e)}")
            return False

class MigrationOrchestrator:
    """Orchestrates the migration process using multiple agents."""
    
    def __init__(self, process_file: str, output_dir: str, package_name: str):
        self.context = MigrationContext(
            process_file=process_file,
            output_dir=output_dir,
            package_name=package_name,
            knowledge_base=ProcessKnowledgeBase()
        )
        
        # Initialize agents
        self.agents = [
            ProcessAnalyzerAgent(self.context),
            CodeGeneratorAgent(self.context),
            ConfigurationAgent(self.context),
            ValidationAgent(self.context)
        ]

    def execute_migration(self) -> bool:
        """Execute the full migration process."""
        success = True
        
        for agent in self.agents:
            logger.info(f"Starting {agent.__class__.__name__}")
            if not agent.process():
                success = False
                logger.error(f"Agent {agent.__class__.__name__} failed")
                break
        
        self._generate_migration_report()
        return success

    def _generate_migration_report(self):
        """Generate a detailed migration report."""
        report = {
            'status': 'success' if not self.context.errors else 'failed',
            'stages_completed': self.context.current_stage,
            'generated_files': list(self.context.generated_files.keys()),
            'errors': self.context.errors,
            'warnings': self.context.warnings
        }
        
        report_path = f"{self.context.output_dir}/migration_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)