# Documentation Modernization Toolkit

A practical Python-based portfolio project demonstrating documentation conversion, Markdown validation, keyword-based knowledge retrieval, and automated quality checks for documentation-as-code workflows.

## Project Overview

This project demonstrates how technical documentation can be prepared for use in a searchable knowledge base. It includes sample support articles, conversion and validation scripts, a search utility, and a Streamlit web interface.

## Key Features

- **Documentation conversion:** Convert sample HTML documentation into Markdown.
- **Markdown validation:** Check documentation files for common quality issues.
- **Knowledge retrieval:** Search Markdown articles using keyword matching and display relevant source content.
- **Source references:** Display source filenames, match scores, and matched terms.
- **Article browser:** Browse the available knowledge articles through a Streamlit interface.
- **Automated checks:** Run validation, unit tests, and Python syntax checks with GitHub Actions.

## Technology Stack

- Python
- Markdown and HTML
- Streamlit
- Git and GitHub
- GitHub Actions
- Python `unittest`

## Repository Structure

```text
documentation-modernization-toolkit/
├── .github/
│   └── workflows/
│       └── validate-docs.yml
├── docs/
│   ├── account-access.md
│   └── password-reset.md
├── sample_source/
├── scripts/
│   ├── convert_docs.py
│   ├── validate_docs.py
│   ├── search_docs.py
│   └── test_search_docs.py
├── app.py
└── requirements.txt
```

## Run Locally

### Prerequisites

- Python 3.10 or compatible version
- Git

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Launch the application

```bash
python -m streamlit run app.py
```

Use the application to search the sample support articles or browse them from the sidebar.

## Run the Documentation Checks

Convert the sample HTML files:

```bash
python scripts/convert_docs.py --input sample_source --output docs
```

Validate the Markdown files:

```bash
python scripts/validate_docs.py
```

Run the search tests:

```bash
python -m unittest discover -s scripts -p "test_*.py" -v
```

Check Python syntax:

```bash
python -m compileall -q scripts
```

## Current Limitations

The search utility uses keyword matching. It does not generate answers with an LLM, use semantic embeddings, or connect to an external chatbot platform. The sample articles are demonstration content rather than production support documentation.

## Purpose

This portfolio project demonstrates practical skills in technical documentation, documentation-as-code, Python scripting, content validation, knowledge retrieval, testing, and continuous integration.

