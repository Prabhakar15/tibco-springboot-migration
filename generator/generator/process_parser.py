"""Parse simplified TIBCO .process XML to extract starters, activities and transitions.
Enhanced with RAG and Agent-based AI for improved accuracy and completeness.
"""
from xml.etree import ElementTree as ET
from typing import Dict, List
import os
import logging
from .ai.migrate import migrate_process
from .ai.rag import ProcessKnowledgeBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

P_NS = '{http://ns.tibco.com/bw/process}'

# Initialize knowledge base
try:
    kb = ProcessKnowledgeBase()
except ImportError:
    logger.warning("AI enhancement libraries not found. Falling back to basic parsing.")
    kb = None


def parse_process(process_path: str) -> Dict:
    tree = ET.parse(process_path)
    root = tree.getroot()

    data = {
        'name': root.get('name'),
        'starters': [],
        'activities': [],
        'transitions': [],
    }
    
    # Try to use AI-enhanced parsing if available
    if kb is not None:
        try:
            logger.info("Using AI-enhanced process parsing")
            kb.index_process_activities(process_path)
            
            # Use RAG to identify complex patterns
            sql_activities = kb.query_similar_activities("SQL database operation", k=5)
            jms_activities = kb.query_similar_activities("JMS messaging operation", k=5)
            rest_activities = kb.query_similar_activities("REST or HTTP service call", k=5)
            
            # Store AI insights in the data
            data['ai_insights'] = {
                'sql_patterns': sql_activities,
                'jms_patterns': jms_activities,
                'rest_patterns': rest_activities
            }
        except Exception as e:
            logger.warning(f"AI-enhanced parsing failed: {str(e)}. Falling back to basic parsing.")

    # starters
    for st in root.findall(f"{P_NS}starter"):
        data['starters'].append({
            'ref': st.get('ref'),
            'name': st.get('name'),
        })

    # activities
    for act in root.findall(f"{P_NS}activity"):
        activity = {
            'name': act.get('name'),
            'type': act.get('type'),
            'config': {}
        }
        
        # Extract SQL details for JDBC activities
        if activity['type'] == 'jdbc':
            sql_elem = act.find(f"{P_NS}sql")
            if sql_elem is not None:
                activity['config']['sql'] = sql_elem.text
                activity['config']['params'] = []
                for param in sql_elem.findall(f"{P_NS}param"):
                    activity['config']['params'].append({
                        'name': param.get('name'),
                        'type': param.get('type'),
                        'value': param.text
                    })
        
        # Extract JMS details
        elif activity['type'] == 'jms':
            jms_elem = act.find(f"{P_NS}jms")
            if jms_elem is not None:
                activity['config'].update({
                    'queue': jms_elem.get('queue'),
                    'connection_factory': jms_elem.get('connection-factory'),
                    'message_type': jms_elem.get('message-type', 'Text'),
                    'delivery_mode': jms_elem.get('delivery-mode', 'PERSISTENT')
                })
                
        # Extract REST/HTTP details
        elif activity['type'] in ('rest', 'http'):
            http_elem = act.find(f"{P_NS}http")
            if http_elem is not None:
                activity['config'].update({
                    'method': http_elem.get('method', 'POST'),
                    'url': http_elem.get('url'),
                    'content_type': http_elem.get('content-type', 'application/json')
                })
        
        # Extract general config
        for c in act.findall('config/*'):
            activity['config'][c.tag.split('}')[-1]] = c.text
            
        data['activities'].append(activity)

    # transitions
    for tr in root.findall(f"{P_NS}transition"):
        data['transitions'].append({
            'from': tr.get('from'),
            'to': tr.get('to'),
            'condition': tr.get('condition')
        })

    return data
