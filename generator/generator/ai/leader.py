"""Leader agent to orchestrate multi-process migration across BW folders.

This module scans the input base dir, creates a ProcessAgent per BW process folder,
and delegates service generation to REST/SOAP service agents. It uses the
ProcessKnowledgeBase for shared RAG knowledge.
"""
from pathlib import Path
from typing import List, Dict
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import zipfile
import os

from .rag import ProcessKnowledgeBase
from .process_agent import ProcessAgent
from .service_agents import RestServiceAgent, SoapServiceAgent
from .hexagonal_agents import HexagonalServiceAgent
from .validation_agent import ValidationAgent
from .packager import Packager

logger = logging.getLogger(__name__)


class LeaderAgent:
    """Orchestrates migration across multiple BW process folders.

    Responsibilities:
    - Scan input base directory for BW process folders
    - Build a shared knowledge base (RAG)
    - Create ProcessAgent for each folder
    - For each process, decide REST vs SOAP (or both) and call respective agents
    - Collect generated files and produce a high-level report
    """

    def __init__(self, input_base: str, output_base: str, package_root: str, parallel: bool = True, max_workers: int = 4, architecture: str = 'layered', service_type: str = 'combined'):
        self.input_base = Path(input_base)
        self.output_base = Path(output_base)
        self.package_root = package_root
        self.kb = ProcessKnowledgeBase()
        self.process_agents: List[ProcessAgent] = []
        self.generated_files: Dict[str, str] = {}
        # collect per-process archives created during execution
        self.process_archives: List[str] = []
        self.parallel = parallel
        self.max_workers = max_workers
        # New: architecture pattern selection
        self.architecture = architecture  # 'layered' or 'hexagonal'
        self.service_type = service_type  # 'rest', 'soap', or 'combined' (for hexagonal)

    def discover_bw_folders(self) -> List[Path]:
        """Discover subfolders under input base that contain BW artifacts.
        A BW folder is assumed if it contains any .process or .bwp or .xsd file.
        """
        result = []
        for child in self.input_base.iterdir():
            if not child.is_dir():
                continue
            has_bw = any(child.glob('*.process')) or any(child.glob('*.bwp')) or any(child.glob('*.xsd'))
            if has_bw:
                result.append(child)
        return result

    def build_shared_knowledge(self, bw_folders: List[Path]):
        """Index all processes into the shared ProcessKnowledgeBase (RAG).
        Indexing is best-effort and will continue even if some files cannot be parsed.
        """
        for folder in bw_folders:
            # attempt to find a .process file
            proc_files = list(folder.glob('*.process'))
            for proc in proc_files:
                try:
                    self.kb.index_process_activities(str(proc))
                except Exception as e:
                    logger.warning(f"Failed to index {proc}: {e}")

    def create_process_agents(self, bw_folders: List[Path]):
        for folder in bw_folders:
            # Use fixed rest/soap output folders instead of per-process folders
            pa = ProcessAgent(folder, self.output_base, self.package_root, self.kb)
            self.process_agents.append(pa)

    def execute(self) -> Dict:
        """Full migration for all discovered BW folders."""
        bw_folders = self.discover_bw_folders()
        logger.info(f"Discovered {len(bw_folders)} BW folders to migrate")

        # Build knowledge base first (helps cross-process pattern recognition)
        self.build_shared_knowledge(bw_folders)

        # Create agents
        self.create_process_agents(bw_folders)

        # For each process, analyze and generate services
        def _process(pa: ProcessAgent):
            result_files = {}
            try:
                context = pa.analyze()
                
                # Route based on architecture selection
                if self.architecture == 'hexagonal':
                    # Use hexagonal architecture (Ports & Adapters pattern)
                    logger.info(f"Generating hexagonal architecture for {pa.folder.name} (service_type: {self.service_type})")
                    hex_agent = HexagonalServiceAgent(context, self.service_type)
                    result_files.update(hex_agent.generate())
                    
                    # Create per-process archive for hexagonal service
                    # Include ALL files from hexagonal generation (not just those with 'hexagonal' in path)
                    try:
                        proc_name = None
                        if getattr(context, 'process_defs', None):
                            if len(context.process_defs) > 0 and isinstance(context.process_defs[0], dict):
                                proc_name = context.process_defs[0].get('name')
                        if not proc_name:
                            proc_name = pa.folder.name
                        
                        # For hexagonal, include ALL generated files (pom.xml, src/, README, etc.)
                        if result_files:
                            zip_path = self.output_base / f"{proc_name}_hexagonal_{self.service_type}.zip"
                            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                                for pth, content in result_files.items():
                                    try:
                                        p = Path(pth)
                                        try:
                                            arcname = str(p.relative_to(self.output_base))
                                        except Exception:
                                            arcname = p.name
                                        zf.writestr(arcname, content)
                                    except Exception:
                                        logger.exception(f"Failed to add {pth} to {zip_path}")
                            logger.info(f"Created hexagonal archive: {zip_path}")
                            self.process_archives.append(str(zip_path))
                    except Exception:
                        logger.exception("Failed to create hexagonal archive")
                else:
                    # Use traditional layered architecture (default)
                    logger.info(f"Generating layered architecture for {pa.folder.name}")
                    service_types = pa.detect_service_types(context)

                    if 'rest' in service_types:
                        rest_agent = RestServiceAgent(context)
                        result_files.update(rest_agent.generate())

                    if 'soap' in service_types:
                        soap_agent = SoapServiceAgent(context)
                        result_files.update(soap_agent.generate())

                    # Collect shared artifacts produced by the process agent
                    result_files.update(pa.generated_files)
                    # Create per-process archives named by the BW process
                    try:
                        # derive process name from parsed context or folder name
                        proc_name = None
                        if getattr(context, 'process_defs', None):
                            if len(context.process_defs) > 0 and isinstance(context.process_defs[0], dict):
                                proc_name = context.process_defs[0].get('name')
                        if not proc_name:
                            proc_name = pa.folder.name

                        # filter generated files by service area and write into zips
                        for svc in ('rest', 'soap'):
                            svc_files = {p: c for p, c in result_files.items() if f"{os.sep}{svc}{os.sep}" in p.replace('/', os.sep)}
                            if not svc_files:
                                continue
                            zip_path = self.output_base / f"{proc_name}_{svc}.zip"
                            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                                for pth, content in svc_files.items():
                                    try:
                                        p = Path(pth)
                                        # compute archive name relative to output_base
                                        try:
                                            arcname = str(p.relative_to(self.output_base))
                                        except Exception:
                                            arcname = p.name
                                        # write string content as utf-8
                                        zf.writestr(arcname, content)
                                    except Exception:
                                        logger.exception(f"Failed to add {pth} to {zip_path}")
                            logger.info(f"Created per-process archive: {zip_path}")
                            self.process_archives.append(str(zip_path))
                    except Exception:
                        logger.exception("Failed to create per-process archives")
            except Exception as e:
                logger.error(f"Migration failed for {pa.folder}: {e}")
            return result_files

        if self.parallel and len(self.process_agents) > 1:
            logger.info(f"Running migration in parallel with {self.max_workers} workers")
            with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
                futures = {ex.submit(_process, pa): pa for pa in self.process_agents}
                for fut in as_completed(futures):
                    files = fut.result()
                    self.generated_files.update(files)
        else:
            for pa in self.process_agents:
                files = _process(pa)
                self.generated_files.update(files)

        # Generate leader-level report
        # Run basic validation and packaging
        validator = ValidationAgent()
        validation_results = validator.validate_projects(self.output_base)

        # Create archives for both REST and SOAP service source code
        packer = Packager()
        archives = []
        
        # Package based on architecture type
        if self.architecture == 'hexagonal':
            # Package hexagonal architecture source code
            hex_path = self.output_base / 'hexagonal'
            if hex_path.exists() and (hex_path / 'src').exists():
                src_zip = self.output_base / f'src_hexagonal_{self.service_type}.zip'
                packer._zip_folder(hex_path / 'src', src_zip)
                archives.append(str(src_zip))
                logger.info(f"Created hexagonal source archive: {src_zip}")
        else:
            # Package REST and SOAP service source code (layered)
            for svc in ['rest', 'soap']:
                svc_path = self.output_base / svc
                if svc_path.exists() and (svc_path / 'src').exists():
                    src_zip = self.output_base / f'src_{svc}.zip'
                    packer._zip_folder(svc_path / 'src', src_zip)
                    archives.append(str(src_zip))
                    logger.info(f"Created {svc.upper()} source archive: {src_zip}")

        # include per-process archives created during processing
        archives.extend(self.process_archives)

        report = {
            'processed_folders': [str(p.folder) for p in self.process_agents],
            'generated_files': list(self.generated_files.keys()),
            'validation': validation_results,
            'archives': archives
        }

        return report
