import importlib, json, traceback, sys
from pathlib import Path

# Ensure the tibco_migration folder (project root containing 'generator') is on sys.path
repo_root = Path(__file__).resolve().parents[4]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

mods = [
    'generator.generator.ai.rag',
    'generator.generator.ai.leader',
    'generator.generator.ai.process_agent',
    'generator.generator.ai.service_agents',
    'generator.generator.ai.run_migration'
]

outputs = {}
for m in mods:
    try:
        importlib.import_module(m)
        outputs[m] = 'OK'
    except Exception:
        outputs[m] = traceback.format_exc()

print(json.dumps(outputs, indent=2))
