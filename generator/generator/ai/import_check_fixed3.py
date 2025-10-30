import importlib, json, traceback, sys
from pathlib import Path

# Find ancestor containing a 'generator' folder and add its parent to sys.path
base = Path(__file__).resolve()
found = False
for _ in range(10):
    candidate = base.parent
    if (candidate / 'generator').is_dir():
        # add parent of candidate (so that 'generator' is importable as top-level)
        sys.path.insert(0, str(candidate.parent))
        found = True
        break
    base = candidate

if not found:
    # fallback: add parents[5]
    repo_root = Path(__file__).resolve().parents[5]
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

print(json.dumps({'sys_path_added': sys.path[0], 'results': outputs}, indent=2))
