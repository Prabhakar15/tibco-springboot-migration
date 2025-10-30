"""Main generator CLI.
Usage:
    python generate.py --input-dir <tibco_artifacts_dir> --output-dir <output_root>

This tool parses XSDs and .process files and generates two Spring Boot projects (REST and SOAP) in parallel.
"""
import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict

from generator.xsd_parser import parse_xsd
from generator.process_parser import parse_process
from generator.templates import DTO_CLASS, CONTROLLER_TEMPLATE, SERVICE_TEMPLATE


def generate_dto_java(package: str, class_name: str, fields: list) -> str:
    imports = set()
    field_lines = []
    getters = []
    setters = []
    for fname, ftype in fields:
        if '.' in ftype:
            imports.add(ftype)
            simple = ftype.split('.')[-1]
        else:
            simple = ftype
        field_lines.append(f'    private {simple} {fname};')
        # getter
        getters.append(f'    public {simple} get{fname[0].upper()+fname[1:]}() {{ return {fname}; }}')
        setters.append(f'    public void set{fname[0].upper()+fname[1:]}({simple} {fname}) {{ this.{fname} = {fname}; }}')

    imports_block = ''
    if imports:
        imports_block = '\n'.join([f'import {i};' for i in sorted(imports)]) + '\n\n'

    content = DTO_CLASS.format(
        package=package,
        imports=imports_block,
        class_name=class_name,
        fields='\n'.join(field_lines),
        getters_setters='\n\n'.join(getters + setters)
    )
    return content


def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def generate_project_from_artifacts(input_dir: str, output_root: str, project_type: str):
    """Generate a simplified Spring Boot project (project_type = 'rest'|'soap')."""
    # scan for XSDs
    xsd_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.xsd')]
    dtos = {}
    for x in xsd_files:
        parsed = parse_xsd(x)
        for name, fields in parsed.items():
            dtos[name] = fields

    base_pkg = 'com.example.tibco_migration'
    src_root = os.path.join(output_root, project_type, 'src', 'main', 'java', *base_pkg.split('.'))
    resources_root = os.path.join(output_root, project_type, 'src', 'main', 'resources')

    # generate DTOs
    for dto_name, fields in dtos.items():
        java_name = dto_name
        content = generate_dto_java(base_pkg, java_name, fields)
        path = os.path.join(src_root, 'dto', f'{java_name}.java')
        write_file(path, content)

    # Parse process files and create a controller/service skeleton
    process_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.process')]
    for pf in process_files:
        proc = parse_process(pf)
        # use loan example defaults
        controller_content = CONTROLLER_TEMPLATE.format(
            package=base_pkg,
            request='LoanApplicationRequest',
            response='LoanApplicationResponse',
            service='LoanApplicationService',
            controller='LoanApplicationController',
            root='loan',
            response_var='LoanApplicationResponse'
        )
        write_file(os.path.join(src_root, 'controller', 'LoanApplicationController.java'), controller_content)

        service_content = SERVICE_TEMPLATE.format(
            package=base_pkg,
            request='LoanApplicationRequest',
            response='LoanApplicationResponse',
            repo='LoanRepository',
            service='LoanApplicationService'
        )
        write_file(os.path.join(src_root, 'service', 'LoanApplicationService.java'), service_content)

    # write a simple pom and application.yml per project
    pom = """<project xmlns=\"http://maven.apache.org/POM/4.0.0\">\n  <modelVersion>4.0.0</modelVersion>\n  <groupId>com.example</groupId>\n  <artifactId>tibco-migration-{ptype}</artifactId>\n  <version>0.1.0</version>\n</project>""".format(ptype=project_type)
    write_file(os.path.join(output_root, project_type, 'pom.xml'), pom)
    write_file(os.path.join(resources_root, 'application.yml'), 'server:\n  port: 8080\n')

    return output_root


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()

    # create projects in parallel
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = [ex.submit(generate_project_from_artifacts, args.input_dir, args.output_dir, 'rest'),
                   ex.submit(generate_project_from_artifacts, args.input_dir, args.output_dir, 'soap')]
        for f in as_completed(futures):
            print('Generated:', f.result())


if __name__ == '__main__':
    main()
