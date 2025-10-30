# TIBCO -> Spring Boot Generator

This Python utility scans a directory of TIBCO artifacts (XSD, .process, WSDL) and generates two Spring Boot skeleton projects (REST and SOAP) in parallel.

Quick start

1. Put your TIBCO XSD and .process files in a folder, e.g. `tibco_artifacts/`.
2. From this generator folder run:

```powershell
python -m generator.generate --input-dir C:\path\to\tibco_artifacts --output-dir C:\path\to\generated_projects
```

What it does

- Parses XSD files and generates simple Java DTO POJOs mapping `xs:string -> String`, `xs:int -> Integer`, `xs:decimal -> BigDecimal`, etc.
- Parses `.process` files to detect starters and basic activities. Generates controller/service skeletons.
- Produces two project folders under `output-dir`: `rest` and `soap`.
- Uses concurrent execution to produce both projects in parallel (multi-agent style).

Limitations

- The XSD parser is intentionally simple and handles typical top-level element with a complexType/sequence. For complex schemas, use `xjc` or extend the parser.
- The generated Java code is a scaffold. Business logic and environment-specific wiring (JNDI, Oracle driver) must be adapted.

Next improvements you can ask me to implement

- Full JAXB generation (xjc) and XML validation against XSD at runtime.
- More complete .process parser mapping TIBCO activities to Java implementations.
- Add tests and CI workflow.
- Generate complete Maven pom.xml with dependencies and build plugins.

If you'd like, I can run the generator on the artifacts you provided earlier and produce the two Spring Boot projects. (I will not commit to git unless you request it.)
