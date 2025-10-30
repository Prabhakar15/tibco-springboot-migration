AI Multi-Agent Migration
========================

Overview
--------
This folder implements an AI-enhanced, multi-agent architecture to migrate TIBCO
BW processes into Spring Boot projects. It supports scanning an input base folder
that contains multiple BW process folders (each with .process/.xsd/.bwp files)
and generates REST and SOAP scaffolding per process.

Key components
--------------
- `leader.py` - LeaderAgent: orchestrates the full migration across folders
- `process_agent.py` - ProcessAgent: analyzes a single BW folder and builds context
- `service_agents.py` - RestServiceAgent / SoapServiceAgent: generate service artifacts
- `rag.py` - ProcessKnowledgeBase: embeddings + vector store (semantic knowledge)
- `run_migration.py` - CLI runner to execute the leader orchestrator

Quick start
-----------
1. Install optional AI dependencies (if you want RAG features):

```powershell
pip install -r generator/generator/ai/requirements.txt
```

2. Run the migration from the repository root:

```powershell
python -m generator.generator.ai.run_migration --input path\to\bw_input --output path\to\output --package com.example.generated
```

Notes
-----
- The generated REST and SOAP artifacts are skeletons intended as a starting
  point. You should extend generated code to match your conventions.
- The RAG features are optional; the system falls back to heuristic parsing
  when AI libraries are not available.
- This implementation is intentionally conservative (safe placeholders) to
  avoid making irreversible changes to production code.

Advanced features
-----------------
- Parallel processing: `LeaderAgent` can run per-process generation in parallel. Pass `parallel=False` to disable or `max_workers` to adjust concurrency.
- SOAP/JAXB support: `SoapServiceAgent` now generates a minimal `pom.xml` with the `maven-jaxb2-plugin` and copies XSDs into `src/main/resources/xsd` so `mvn generate` will create JAXB classes.
- Validation: `ValidationAgent` can detect generated projects and optionally run `mvn -DskipTests package` to compile them (Maven must be available on PATH).
- Packaging: `Packager` zips each generated project under the output base into `output/<project>.zip`.

Extending the system
--------------------
- Add richer WSDL/JAXB generation based on XSDs in `SoapServiceAgent`.
- Improve entity generation and mapping in `RestServiceAgent`.
- Add parallel/async execution in `LeaderAgent` for speed.
- Add tests and validation hooks in `ValidationAgent` (future work).
