import importlib, json, traceback

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
    except Exception as e:
        outputs[m] = traceback.format_exc()

print(json.dumps(outputs, indent=2))
