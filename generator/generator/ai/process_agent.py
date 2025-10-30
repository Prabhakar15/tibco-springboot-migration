"""Agent that analyzes a single BW process folder and produces a process context.

The ProcessAgent reads .process files, XSDs and BWP resources (if present) and builds
an internal context that service generators (REST/SOAP) can use.
"""
from pathlib import Path
from typing import Dict, Any, List
import logging
import json

from .rag import ProcessKnowledgeBase

try:
    # import existing parser (fallback to simple parsing if not available)
    from ..process_parser import parse_process
except Exception:
    def parse_process(p):
        return {'name': Path(p).stem, 'activities': []}

logger = logging.getLogger(__name__)


class ProcessContext:
    def __init__(self, folder: Path, output_folder: Path, package_root: str, kb: ProcessKnowledgeBase):
        self.folder = folder
        self.output_folder = output_folder
        self.package_root = package_root
        self.kb = kb
        self.process_defs: List[Dict[str, Any]] = []
        self.schemas: List[Path] = []
        self.resources: List[Path] = []
        self.generated_files: Dict[str, str] = {}
        self.service_hints: List[str] = []


class ProcessAgent:
    """Analyze a BW folder and produce a ProcessContext."""

    def __init__(self, folder: Path, output_folder: Path, package_root: str, kb: ProcessKnowledgeBase):
        self.folder = folder
        self.output_folder = output_folder
        self.package_root = package_root
        self.kb = kb
        self.generated_files: Dict[str, str] = {}

    def analyze(self) -> ProcessContext:
        ctx = ProcessContext(self.folder, self.output_folder, self.package_root, self.kb)

        # collect artifacts
        ctx.schemas = list(self.folder.glob('*.xsd'))
        ctx.resources = list(self.folder.glob('*.bwp'))
        proc_files = list(self.folder.glob('*.process'))

        # parse each process file
        for p in proc_files:
            try:
                parsed = parse_process(str(p))
                ctx.process_defs.append(parsed)
            except Exception as e:
                logger.warning(f"Failed to parse {p}: {e}")

        # Save a small context file for traceability
        try:
            self.folder.mkdir(parents=True, exist_ok=True)
            ctx_json = json.dumps({'processes': [pd.get('name') for pd in ctx.process_defs]}, indent=2)
            ctx.generated_files[str(self.output_folder / 'process_context.json')] = ctx_json
        except Exception:
            pass

        # Derive simple service hints from parsed activities using KB if available
        if self.kb:
            try:
                for pd in ctx.process_defs:
                    # query for REST/JMS/SQL patterns per process name
                    rest_hits = self.kb.query_similar_activities('REST or HTTP service call', k=3)
                    jms_hits = self.kb.query_similar_activities('JMS messaging operation', k=3)
                    sql_hits = self.kb.query_similar_activities('SQL database operation', k=3)

                    # heuristics: if rest_hits found -> rest
                    if rest_hits:
                        ctx.service_hints.append('rest')
                    if jms_hits:
                        ctx.service_hints.append('jms')
                    if sql_hits:
                        ctx.service_hints.append('sql')
            except Exception as e:
                logger.debug(f"KB lookup failed: {e}")

        return ctx

    def detect_service_types(self, context: ProcessContext) -> List[str]:
        """Return a list of service types detected for this process (e.g., ['rest','soap']).
        Current detection is heuristic: if XSDs are present or process hints mention SOAP-like
        elements, prefer SOAP; if HTTP activity present, prefer REST. Both can be returned.
        """
        types = set()

        # If there are XSDs and WSDL-like hints, include soap
        if context.schemas:
            types.add('soap')

        # If any process mentions HTTP/rest in their activity names, prefer rest
        for pd in context.process_defs:
            for act in pd.get('activities', []):
                t = act.get('type', '').lower()
                name = act.get('name', '').lower()
                if 'http' in t or 'rest' in t or 'http' in name or 'rest' in name:
                    types.add('rest')

        # If no explicit detection, default to rest (configurable later)
        if not types:
            types.add('rest')

        return list(types)
