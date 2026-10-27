# Documentation Modernization Toolkit

A small portfolio project demonstrating a repeatable workflow for transforming sample legacy HTML documentation into Markdown suitable for a chatbot knowledge base.

## What it demonstrates
- Python scripting with the standard library
- HTML-to-Markdown conversion for common documentation elements
- Consistent YAML-style front matter
- Validation of required metadata, internal links, and image references
- Git-based documentation-as-code workflow
- A foundation for CI validation with GitHub Actions

## Scope and limitations
This is a **local demo using sample HTML pages**, not a live Confluence integration. Real Confluence migrations require access to a Confluence export/API and environment-specific authentication. The converter intentionally handles a small, documented subset of HTML rather than every possible page layout.

## Quick start
Requires Python 3.10+.

```bash
python scripts/convert_docs.py --input sample_source --output docs
python scripts/validate_docs.py --docs docs --report reports/validation-report.md
```

The conversion script creates Markdown files in `docs/`. The validator writes a report and exits with a non-zero status if it finds errors.

## Project structure
```text
documentation-modernization-toolkit/
├── sample_source/       # Sample legacy HTML pages
├── scripts/             # Conversion and validation utilities
├── docs/                # Generated Markdown knowledge articles
├── templates/           # Reusable article template
├── standards/           # Migration and authoring standards
├── reports/             # Validation report output
└── .github/workflows/   # Automated validation
```

## Suggested demo
1. Run the converter.
2. Inspect generated Markdown and front matter.
3. Run the validator and review the report.
4. Deliberately break a link or remove a required metadata field, then rerun validation.
5. Commit the changes to Git and explain the workflow in a portfolio walkthrough.

## Future enhancements
- Parse a real Confluence HTML/XML export
- Add richer table and macro handling
- Add automated tests
- Use GitHub Copilot to propose improvements, then review and test them
- Publish with Backstage TechDocs or another documentation portal
