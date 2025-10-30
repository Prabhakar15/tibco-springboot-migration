"""RAG (Retrieval Augmented Generation) implementation for TIBCO process analysis.

This module provides a full implementation when optional AI libraries are
installed (numpy, sentence-transformers, faiss). When those libraries are not
available the module exposes a lightweight fallback `ProcessKnowledgeBase` that
logs warnings and provides no-op behavior so the rest of the generator can
import and run without hard dependency on ML libraries.
"""

from typing import List, Dict, Any
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)


# Try to import heavy ML dependencies; if unavailable, provide a safe fallback.
try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    import faiss

    class ProcessKnowledgeBase:
        """Full featured KB using embeddings + FAISS."""

        def __init__(self):
            # Initialize the embedding model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            # dimension of the chosen model may vary; use model.get_sentence_embedding_dimension() if needed
            self.dimension = 384
            self.index = faiss.IndexFlatL2(self.dimension)
            self.activities_data: List[Dict[str, Any]] = []

        def index_process_activities(self, process_file: str):
            """Index activities from a TIBCO process file into the vector store."""
            tree = ET.parse(process_file)
            root = tree.getroot()

            activities = root.findall(".//Activity")
            for activity in activities:
                activity_data = {
                    'type': activity.get('type'),
                    'name': activity.get('name'),
                    'config': self._extract_config(activity),
                    'transitions': self._extract_transitions(activity)
                }

                text_repr = self._create_text_representation(activity_data)
                embedding = self.model.encode([text_repr])[0]
                self.index.add(np.array([embedding]).astype('float32'))
                self.activities_data.append(activity_data)

        def query_similar_activities(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
            query_embedding = self.model.encode([query])[0]
            distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), k)
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.activities_data):
                    res = self.activities_data[idx].copy()
                    res['similarity_score'] = float(1 / (1 + dist))
                    results.append(res)
            return results

        def _extract_config(self, activity: ET.Element) -> Dict[str, Any]:
            config = {}
            for config_node in activity.findall(".//ConfigValue"):
                key = config_node.get('key')
                value = config_node.text
                config[key] = value
            return config

        def _extract_transitions(self, activity: ET.Element) -> List[Dict[str, str]]:
            transitions = []
            for transition in activity.findall(".//Transition"):
                transitions.append({
                    'from': transition.get('from'),
                    'to': transition.get('to'),
                    'condition': transition.get('condition')
                })
            return transitions

        def _create_text_representation(self, activity_data: Dict[str, Any]) -> str:
            parts = [f"Activity type: {activity_data.get('type')}", f"Activity name: {activity_data.get('name')}"]
            for key, value in activity_data.get('config', {}).items():
                parts.append(f"Config {key}: {value}")
            for transition in activity_data.get('transitions', []):
                parts.append(f"Transition from {transition.get('from')} to {transition.get('to')}")
                if transition.get('condition'):
                    parts.append(f"Condition: {transition.get('condition')}")
            return " | ".join(parts)

except Exception as e:  # pragma: no cover - fallback when ML libs are not installed
    logger.warning(f"AI libs not available ({e}); using fallback ProcessKnowledgeBase.")

    class ProcessKnowledgeBase:
        """Fallback KB that provides no-op indexing and empty query results.

        This allows the rest of the migration pipeline to run without ML
        dependencies. The fallback logs warnings when methods are used.
        """

        def __init__(self):
            self.activities_data: List[Dict[str, Any]] = []

        def index_process_activities(self, process_file: str):
            logger.info(f"(fallback) index_process_activities called for {process_file}; no-op")

        def query_similar_activities(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
            logger.info(f"(fallback) query_similar_activities called for query='{query}'")
            return []

        # Keep methods signatures consistent with full implementation
        def _extract_config(self, activity: ET.Element) -> Dict[str, Any]:
            return {}

        def _extract_transitions(self, activity: ET.Element) -> List[Dict[str, str]]:
            return []

        def _create_text_representation(self, activity_data: Dict[str, Any]) -> str:
            return ''