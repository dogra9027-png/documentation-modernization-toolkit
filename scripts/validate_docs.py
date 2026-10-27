
from pathlib import Path
import re
import sys

DOCS_DIR = Path("docs")

REQUIRED_FIELDS = [
    "title",
    "slug",
    "content_type",
    "audience",
    "tags",
    "review_date",
]


def validate_file(path):
    """Return a list of validation errors for one Markdown article."""
    errors = []
    text = path.read_text(encoding="utf-8")

    # Check YAML-style front matter.
    if not text.startswith("---\n"):
        errors.append("Missing front matter opening delimiter.")
        return errors

    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append("Front matter is not closed with ---.")
        return errors

    front_matter = parts[1]
    body = parts[2].strip()

    for field in REQUIRED_FIELDS:
        if not re.search(rf"(?m)^{re.escape(field)}\s*:", front_matter):
            errors.append(f"Missing required metadata field: {field}")

    # Check that the article has a useful body.
    if not body:
        errors.append("Article body is empty.")

    # Check headings.
    if not re.search(r"(?m)^#\s+\S", body):
        errors.append("Missing H1 title heading.")

    if re.search(r"(?m)^\*\*#{1,6}\s", body):
        errors.append("Heading has unwanted bold formatting.")

    # Check Markdown links.
    for target in re.findall(r"\]\((.*?)\)", body):
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue

        local_target = target.split("#", 1)[0].split("?", 1)[0]
        if not local_target:
            continue

        destination = (path.parent / local_target).resolve()
        if not destination.exists():
            errors.append(f"Broken local link: {target}")

    # Check for common conversion leftovers.
    if re.search(r"<(?:div|p|h[1-6]|ul|ol|li)\b", body, re.IGNORECASE):
        errors.append("HTML tags remain in the Markdown body.")

    if re.search(r"(?m)^\\-", body):
        errors.append("List markers contain unnecessary escaping.")

    return errors


def main():
    if not DOCS_DIR.exists():
        print(f"ERROR: Documentation folder not found: {DOCS_DIR}")
        sys.exit(1)

    files = sorted(DOCS_DIR.glob("*.md"))
    if not files:
        print(f"ERROR: No Markdown files found in {DOCS_DIR}")
        sys.exit(1)

    total_errors = 0

    for path in files:
        errors = validate_file(path)

        if errors:
            print(f"FAIL: {path}")
            for error in errors:
                print(f"  - {error}")
            total_errors += len(errors)
        else:
            print(f"PASS: {path}")

    print(f"\nChecked {len(files)} file(s); found {total_errors} issue(s).")

    if total_errors:
        sys.exit(1)

    print("All documentation checks passed.")


if __name__ == "__main__":
    main()
