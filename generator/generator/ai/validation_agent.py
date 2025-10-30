"""ValidationAgent: validates generated projects.

This agent performs lightweight checks on generated projects and can optionally
invoke Maven to compile them if Maven is available on PATH. It returns a summary
per project folder about success/failure and captured output.
"""
from pathlib import Path
import subprocess
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ValidationAgent:
    def __init__(self, mvn_cmd: str = 'mvn'):
        self.mvn_cmd = mvn_cmd

    def _find_projects(self, output_base: Path) -> List[Path]:
        # A project is any folder that contains a pom.xml or src folder
        projects = []
        for child in output_base.iterdir():
            if not child.is_dir():
                continue
            if (child / 'pom.xml').exists() or (child / 'src').is_dir():
                projects.append(child)
        return projects

    def validate_projects(self, output_base: str) -> Dict[str, Any]:
        out = Path(output_base)
        results = {}
        projects = self._find_projects(out)
        for p in projects:
            results[str(p)] = self._validate_project(p)
        return results

    def _validate_project(self, project_path: Path) -> Dict[str, Any]:
        res = {'compiled': False, 'mvn_available': False, 'mvn_output': ''}
        # Check for pom.xml
        if not (project_path / 'pom.xml').exists():
            res['mvn_output'] = 'No pom.xml present; skipping mvn'
            return res

        # Try to run mvn -DskipTests package
        try:
            # Check mvn is available
            mvn_check = subprocess.run([self.mvn_cmd, '--version'], capture_output=True, text=True)
            if mvn_check.returncode != 0:
                res['mvn_output'] = 'Maven not available or returned non-zero on --version'
                return res
            res['mvn_available'] = True

            proc = subprocess.run([self.mvn_cmd, '-DskipTests', 'package'], cwd=str(project_path), capture_output=True, text=True)
            res['mvn_output'] = proc.stdout + '\n' + proc.stderr
            res['compiled'] = proc.returncode == 0
            return res
        except FileNotFoundError:
            res['mvn_output'] = 'Maven executable not found'
            return res
        except Exception as e:
            res['mvn_output'] = f'Exception running mvn: {e}'
            return res
